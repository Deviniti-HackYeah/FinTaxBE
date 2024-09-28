from datetime import datetime
from typing import Any, Dict

from sqlalchemy import String, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

DbBase = declarative_base()


class ConversationTurnDB(DbBase):
    __tablename__ = 'conversation_turns'
    id: Mapped[str] = mapped_column(String, primary_key=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    returned_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    request: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    requested_intent: Mapped[str] = mapped_column(String, nullable=False)
    stats: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
