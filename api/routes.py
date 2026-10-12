
from pathlib import Path
import sys
import time
from threading import Lock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from fastapi import APIRouter, HTTPException
from api.schemas import (
    AskRequest,
    AskResponse,
    AgentChatRequest,
    AgentChatResponse,
)
from api.logging_config import logger
from agents.rag_agent import RAGAgent

router = APIRouter()
agent = RAGAgent()

# Temporary in-memory conversation history, separated by session ID.
chat_sessions = {}
chat_sessions_lock = Lock()

MAX_HISTORY_MESSAGES = 10


def rewrite_follow_up(message: str, history: list) -> str:
    """Rewrite a follow-up into a standalone question using session history."""
    if not history:
        return message

    history_text = "\n".join(
        f"{item['role'].capitalize()}: {item['content']}"
        for item in history
    )

    prompt = f"""
Rewrite the latest user question as a standalone question.

Use the conversation history to resolve references such as
"it", "this", "that", "they", and "those".

Do not answer the question.
Do not add information that is not supported by the history.
Return only the rewritten question.

Conversation history:
{history_text}

Latest user question:
{message}

Standalone question:
"""

    try:
        response = agent.cohere_chat(
            messages=[{"role": "user", "content": prompt}]
        )
        rewritten = response.message.content[0].text.strip()
        return rewritten or message
    except Exception:
        logger.exception("Follow-up question rewriting failed")
        return message


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    start_time = time.time()
    logger.info("Request received | endpoint=/ask")

    try:
        result = agent.ask(request.question)

        response = AskResponse(
            question=result.get("question") or request.question,
            answer=result.get("answer") or "No answer generated.",
            tool=result.get("tool") or "knowledge_search",
            sources=result.get("sources") or [],
        )

        logger.info(
            "Request completed | endpoint=/ask | time=%.2fs",
            time.time() - start_time,
        )
        return response

    except Exception:
        logger.exception("Request failed | endpoint=/ask")
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


@router.post("/agent/chat", response_model=AgentChatResponse)
def agent_chat(request: AgentChatRequest):
    start_time = time.time()
    session_id = request.session_id
    message = request.message

    try:
        # Copy history while holding the lock.
        with chat_sessions_lock:
            history = list(chat_sessions.get(session_id, []))

        # Resolve follow-ups before searching the knowledge base.
        standalone_question = rewrite_follow_up(message, history)

        logger.info(
            "Agent chat | session_id=%s | rewritten_question=%s",
            session_id,
            standalone_question,
        )

        result = agent.ask(standalone_question)

        answer = result.get("answer") or "No answer generated."

        # Save the original user message and the assistant response.
        with chat_sessions_lock:
            current_history = chat_sessions.setdefault(session_id, [])
            current_history.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": answer},
            ])

            # Keep only the most recent messages.
            chat_sessions[session_id] = current_history[-MAX_HISTORY_MESSAGES:]

        response = AgentChatResponse(
            session_id=session_id,
            message=message,
            answer=answer,
            tool=result.get("tool") or "knowledge_search",
            sources=result.get("sources") or [],
        )

        logger.info(
            "Agent chat completed | session_id=%s | time=%.2fs",
            session_id,
            time.time() - start_time,
        )
        return response

    except Exception:
        logger.exception(
            "Agent chat failed | session_id=%s",
            session_id,
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )
