from datetime import datetime
from typing import Any, Dict

from sqlalchemy import JSON, DateTime, String, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

DbBase = declarative_base()


class ConversationTurnDB(DbBase):  # type: ignore
    __tablename__ = "conversation_turns"
    session_id: Mapped[str] = mapped_column(String, primary_key=True)
    turn_id: Mapped[str] = mapped_column(String, primary_key=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    returned_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_action: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    full_response: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    requested_intent: Mapped[str] = mapped_column(String, nullable=True)
    stats: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
