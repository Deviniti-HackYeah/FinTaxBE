import datetime
from typing import Any, Dict

from pydantic import BaseModel


class ConversationTurn(BaseModel):
    id: str
    requested_at: datetime.datetime
    returned_at: datetime.datetime
    request: str
    response: str
    requested_intent: str
    stats: Dict[str, Any]
