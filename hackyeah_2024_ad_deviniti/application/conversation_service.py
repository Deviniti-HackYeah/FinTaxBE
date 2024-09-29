import datetime
import uuid
from typing import List

from hackyeah_2024_ad_deviniti.application.ai_processor.situation_verificator import (
    SituationVerification,
)
from hackyeah_2024_ad_deviniti.domain.conwersation_turn import ConversationTurn
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.infrastructure.database.repository import (
    ConversationTurnRepository,
)
from hackyeah_2024_ad_deviniti.presentation.dto import (
    TextResponses,
    TurnResponseFullDto,
)


class ConversationService:
    _conversation_repository: ConversationTurnRepository

    def __init__(self, conversation_repository: ConversationTurnRepository) -> None:
        self._conversation_repository = conversation_repository

    async def run_turn(
        self, session_id: str, action: UserAction
    ) -> ConversationTurn:
        start_time = datetime.datetime.now()
        response_full = await self.process_for_response(session_id, action)
        turn = ConversationTurn(
            session_id=session_id,
            turn_id=str(uuid.uuid1()),
            requested_at=start_time,
            returned_at=datetime.datetime.now(),
            user_action=action,
            full_response=response_full,
            requested_intent=None,
            stats={},
        )
        self._conversation_repository.add_conversation_turn(turn)
        return response_full

    async def process_for_response(
        self, session_id: str, action: UserAction
    ) -> TurnResponseFullDto:
        history = self.get_history_turns(session_id)
        if len(history) == 0:
            return await self.process_for_response(session_id, action)
        else:
            raise Exception()

    async def process_conversation_init(
        self, action: UserAction
    ) -> TurnResponseFullDto:
        process_result = await SituationVerification().call(action.value)
        response_start = (
            "Twoje zapytanie dotyczy wniosku PCC-3."
            if process_result.is_ok
            else "Twoje zapytanie nie dotyczy wniosku PCC-3."
        )
        response = f"{response_start}\n\n{process_result.justification_in_polish}"
        return TurnResponseFullDto(
            response=TextResponses(
                agent_1=response,
                agent_2="Dołączam dokument który pokazuje wniosek PCC-3, czy chcesz go wypełnić?",
            ),
            sources=[],
            extras=None,
        )

    def get_history_turns(self, session_id: str) -> List[ConversationTurn]:
        return self._conversation_repository.get_conversation_turns_by_id(session_id)

    async def save(self, turn: ConversationTurn) -> None:
        self._conversation_repository.add_conversation_turn(conversation_turn=turn)
