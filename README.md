# Enterprise Knowledge Base RAG Agent

An AI-powered knowledge assistant that helps organizations retrieve accurate, context-aware answers from internal documents using Retrieval-Augmented Generation (RAG).

## Overview

The Enterprise Knowledge Base RAG Agent allows users to ask questions about company policies, IT support, customer support procedures, and product documentation. Instead of manually searching through multiple documents, users receive relevant answers with source references.

The project combines semantic search, vector retrieval, reranking, conversation memory, and an AI agent to make enterprise knowledge more accessible.

## Features

- **Document Ingestion:** Loads and processes enterprise PDF documents.
- **Text Chunking:** Splits documents into manageable chunks for retrieval.
- **Semantic Search:** Uses Sentence Transformers to generate text embeddings.
- **Vector Database:** Uses FAISS for similarity-based document retrieval.
- **AI-Powered Answers:** Uses Cohere to generate answers grounded in retrieved content.
- **Intelligent Agent:** Supports knowledge search, policy search, and document summarization tools.
- **Conversation Memory:** Supports contextual follow-up questions within a session.
- **Source References:** Returns document names, categories, page numbers, and relevance scores.
- **Reranking and Evaluation:** Includes retrieval evaluation and reranking experiments.
- **REST API:** Provides FastAPI endpoints for questions, conversations, and health checks.
- **Docker Support:** Packages the application into a container for consistent execution.

## Technology Stack

- **Language:** Python
- **LLM Provider:** Cohere
- **RAG Framework:** LangChain
- **Embedding Model:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Store:** FAISS
- **Reranking:** Cross-Encoder
- **Backend:** FastAPI
- **Containerization:** Docker
- **Testing:** Pytest

## Knowledge Base Categories

The project includes sample documents covering:

- **HR:** Employee policies, casual leave, and work-from-home policies.
- **IT:** Password resets, VPN support, and account management.
- **Support:** Complaint handling, ticket escalation, and customer support procedures.
- **Products:** Product manuals, FAQs, and warranty policies.

## Project Structure

```text
enterprise-rag-agent/
├── api/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   └── logging_config.py
├── data/
│   ├── raw/
│   │   ├── hr/
│   │   ├── it/
│   │   ├── support/
│   │   └── products/
│   └── document_inventory.csv
├── evaluation/
├── src/
│   ├── agents/
│   ├── embeddings/
│   ├── ingestion/
│   ├── rag/
│   ├── retrieval/
│   ├── tools/
│   └── vectorstore/
├── tests/
├── .env.example
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Eshwarguthurthi/enterprise-rag-agent.git
cd enterprise-rag-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a template.

```env
COHERE_API_KEY=your_cohere_api_key_here
```

Replace the placeholder with your own Cohere API key. Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
uvicorn api.main:app --reload
```

The API will be available at:

- Root: http://localhost:8000/
- Health check: http://localhost:8000/health
- Interactive API documentation: http://localhost:8000/docs

## Docker Deployment

Build the Docker image:

```bash
docker build -t enterprise-rag-agent .
```

Run the container:

```bash
docker run -d --name enterprise-rag-agent-container -p 8001:8000 --env-file .env enterprise-rag-agent
```

Verify the health endpoint:

http://localhost:8001/health

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check the API root |
| GET | `/health` | Check service health |
| POST | `/ask` | Ask a knowledge-base question |
| POST | `/agent/chat` | Chat with session-based context |

### Example: Ask a Question

**POST** `/ask`

```json
{
  "question": "How many casual leave days do employees get?"
}
```

Example response:

```json
{
  "question": "How many casual leave days do employees get?",
  "answer": "Employees are entitled to 12 casual leave days per calendar year.",
  "tool": "policy_search",
  "sources": [
    {
      "source": "leave_policy.pdf",
      "category": "hr",
      "page": 1,
      "score": 0.74
    }
  ]
}
```

The response above illustrates the expected structure; retrieval scores and source lists may vary.

### Example: Agent Chat

**POST** `/agent/chat`

```json
{
  "session_id": "demo-session-001",
  "message": "How many casual leave days do employees get?"
}
```

Use the same `session_id` for follow-up questions. A new session starts without the previous session's conversation history.

## Evaluation and Testing

The repository includes evaluation scripts for retrieval performance and reranking experiments, along with API tests.

Run the tests using:

```bash
pytest -v
```

Run the evaluation scripts from the project root as appropriate:

```bash
python evaluation/evaluate_retrieval.py
python evaluation/evaluate_reranker.py
```

## Security Notes

- Keep API keys in environment variables.
- Never commit `.env` or other files containing secrets.
- Use authentication and HTTPS before exposing the API publicly.
- In-memory conversation history is temporary and may be lost when the application restarts.

## Future Enhancements

- Persistent conversation storage.
- User authentication and role-based access control.
- Document upload and knowledge-base management APIs.
- Cloud deployment and production monitoring.
- Improved retrieval evaluation and automated testing.

## Author

**Eshwar Prasad Guthurthi**

GitHub: https://github.com/Eshwarguthurthi

## License

Add a license file if you intend to distribute this project under an open-source license.
