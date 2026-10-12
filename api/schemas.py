
from pydantic import BaseModel, Field, field_validator


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Question cannot be empty.")
        return value


class AskResponse(BaseModel):
    question: str
    answer: str
    tool: str
    sources: list


class AgentChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=3, max_length=500)

    @field_validator("session_id", "message")
    @classmethod
    def strip_values(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class AgentChatResponse(BaseModel):
    session_id: str
    message: str
    answer: str
    tool: str
    sources: list
