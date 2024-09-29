from typing import List

from hackyeah_2024_ad_deviniti.application.form_flow.form_a import (
    CelZlozeniaStep,
    DateStep,
    PodmiotSkladajacyjStep,
)
from hackyeah_2024_ad_deviniti.domain.conversation_turn import (
    ConversationTurn,
    TurnResult,
)
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction

ALL_STEPS = [DateStep(), CelZlozeniaStep(), PodmiotSkladajacyjStep()]


async def call_for_fill(
        action: UserAction, history: List[ConversationTurn]
) -> TurnResult:
    for it in ALL_STEPS:
        if it.choose_this_step(history, action):
            return await it.process_step(action, history)
    raise Exception()
