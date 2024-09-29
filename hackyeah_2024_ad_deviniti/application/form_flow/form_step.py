from abc import ABC, abstractmethod
from typing import List

from hackyeah_2024_ad_deviniti.domain.conversation_turn import (
    ConversationTurn,
    TurnResult,
)
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction


class DialogStep(ABC):

    @abstractmethod
    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        pass

    @abstractmethod
    async def process_step(
        self,
        user_action: UserAction,
        previous_turns: List[ConversationTurn],
    ) -> TurnResult:
        pass
