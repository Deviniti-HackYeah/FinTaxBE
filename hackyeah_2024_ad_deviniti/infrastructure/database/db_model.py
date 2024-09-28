from datetime import datetime

from sqlalchemy.orm import declarative_base

DbBase = declarative_base()


class ConversationTurnDB(DbBase):
    __tablename__ = 'conversation_turns'
    id: str
    requested_at: datetime
    returned_at: datetime
    request: str
    response: str
    requested_intent: str
    stats: str
