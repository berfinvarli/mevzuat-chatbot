from pydantic import BaseModel, Field

from app.core.constants import (
    DEFAULT_OPENAI_MODEL,
    MAX_TOOL_ITERATIONS,
    STREAM_TOKEN_DELAY,
)
from app.core.prompts import SYSTEM_PROMPT


class RuntimeSettings(BaseModel):
    system_prompt: str
    openai_model: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1)
    max_tool_iterations: int = Field(ge=1, le=50)
    stream_token_delay: float = Field(ge=0.0, le=1.0)

    @classmethod
    def defaults(cls) -> "RuntimeSettings":
        return cls(
            system_prompt=SYSTEM_PROMPT,
            openai_model=DEFAULT_OPENAI_MODEL,
            temperature=1.0,
            max_tokens=None,
            max_tool_iterations=MAX_TOOL_ITERATIONS,
            stream_token_delay=STREAM_TOKEN_DELAY,
        )


class RuntimeSettingsUpdate(BaseModel):
    system_prompt: str | None = None
    openai_model: str | None = None
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1)
    max_tool_iterations: int | None = Field(default=None, ge=1, le=50)
    stream_token_delay: float | None = Field(default=None, ge=0.0, le=1.0)
