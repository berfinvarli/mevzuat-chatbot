from pydantic import BaseModel, field_validator

from app.schemas.message import Message


class ChatRequest(BaseModel):
    messages: list[Message]

    @field_validator("messages")
    @classmethod
    def messages_not_empty(cls, v: list[Message]) -> list[Message]:
        if not v:
            raise ValueError("mesaj boş olamaz")
        return v
