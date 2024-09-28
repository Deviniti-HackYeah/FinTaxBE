import datetime

from pydantic import BaseModel


class ConversationTurn(BaseModel):
    id: str
    requested_at: datetime.datetime
    returned_at: datetime.datetime
    request: str
    response: str
    stats: str
