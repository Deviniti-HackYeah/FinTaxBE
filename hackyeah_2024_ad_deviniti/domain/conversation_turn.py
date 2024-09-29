import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.presentation.dto import TurnResponseFullDto


class ConversationTurn(BaseModel):
    session_id: str
    turn_id: str
    requested_at: datetime.datetime
    returned_at: datetime.datetime
    user_action: UserAction
    full_response: TurnResponseFullDto
    requested_intent: Optional[str]
    stats: Dict[str, Any]


class TurnResult(BaseModel):
    full_response: TurnResponseFullDto
    intent: Optional[str]
