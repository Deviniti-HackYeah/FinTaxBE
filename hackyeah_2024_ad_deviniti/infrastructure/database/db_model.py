from datetime import datetime

from pydantic import BaseModel


class ConversationTurnDB(BaseModel):
    id: str
    requested_at: datetime
    returned_at: datetime
    request: str
    response: str
    requested_intent: str
    stats: str
