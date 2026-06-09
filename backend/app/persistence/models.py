from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.postgres import Base


class AppSettings(Base):
    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    system_prompt: Mapped[str] = mapped_column(Text)
    openai_model: Mapped[str] = mapped_column(String(128))
    temperature: Mapped[float] = mapped_column(Float)
    max_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_tool_iterations: Mapped[int] = mapped_column(Integer)
    stream_token_delay: Mapped[float] = mapped_column(Float)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    updated_by: Mapped[str | None] = mapped_column(String(128), nullable=True)


class CmsEntry(Base):
    __tablename__ = "cms"

    key: Mapped[str] = mapped_column(String(128), primary_key=True)
    value: Mapped[str] = mapped_column(Text)
