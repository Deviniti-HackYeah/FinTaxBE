import datetime
import uuid
from typing import List

from loguru import logger

from hackyeah_2024_ad_deviniti.application.ai_processor.situation_verificator import (
    SituationVerification,
)
from hackyeah_2024_ad_deviniti.application.intents import (
    CORRECT_FOR_PCC_3,
    INCORRECT_SITUATION,
    SITUATION_ADDITIONAL_QUESTION,
)
from hackyeah_2024_ad_deviniti.domain.conwersation_turn import (
    ConversationTurn,
    TurnResult,
)
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.infrastructure.database.repository import (
    ConversationTurnRepository,
)
from hackyeah_2024_ad_deviniti.presentation.dto import (
    DocumentPayload,
    QuestionExtrasDocument,
    TextResponses,
    TurnResponseFullDto,
)


class ConversationService:
    _conversation_repository: ConversationTurnRepository

    def __init__(self, conversation_repository: ConversationTurnRepository) -> None:
        self._conversation_repository = conversation_repository

    async def run_turn(self, session_id: str, action: UserAction) -> ConversationTurn:
        start_time = datetime.datetime.now()
        turn_result = await self.process_for_response(session_id, action)
        turn = ConversationTurn(
            session_id=session_id,
            turn_id=str(uuid.uuid1()),
            requested_at=start_time,
            returned_at=datetime.datetime.now(),
            user_action=action,
            full_response=turn_result.full_response,
            requested_intent=turn_result.intent,
            stats={},
        )
        self._conversation_repository.add_conversation_turn(turn)
        return turn

    async def process_for_response(
        self, session_id: str, action: UserAction
    ) -> TurnResult:
        history = self.get_history_turns(session_id)
        logger.info(history)
        last_intent = history[-1].requested_intent if history else None
        if len(history) == 0 or (
            last_intent
            and last_intent in [SITUATION_ADDITIONAL_QUESTION, INCORRECT_SITUATION]
        ):
            return await self.process_conversation_init(action, history)
        else:
            raise Exception()

    async def process_conversation_init(
        self, action: UserAction, history: List[ConversationTurn]
    ) -> TurnResult:
        process_result = await SituationVerification().call(action.value, history)
        response_start = (
            "Twoje zapytanie dotyczy wniosku PCC-3."
            if process_result.is_ok
            else (
                process_result.additional_question
                if process_result.should_ask_additional_question
                else "Twoje zapytanie nie dotyczy wniosku PCC-3."
            )
        )
        intent = (
            CORRECT_FOR_PCC_3
            if process_result.is_ok
            else (
                SITUATION_ADDITIONAL_QUESTION
                if process_result.should_ask_additional_question
                else INCORRECT_SITUATION
            )
        )
        response = f"{response_start}\n\n{process_result.justification_in_polish}"
        return TurnResult(
            full_response=TurnResponseFullDto(
                response=TextResponses(
                    agent_1=response,
                    agent_2="Dołączam dokument który pokazuje wniosek PCC-3, czy chcesz go wypełnić?",
                ),
                sources=[],
                extras=[
                    QuestionExtrasDocument(
                        type="document",
                        payload=DocumentPayload(
                            title="pcc-3.pdf",
                            url="https://www.podatki.gov.pl/media/4135/pcc-3-05-012.pdf",
                        ),
                    )
                ] if CORRECT_FOR_PCC_3 == intent else [],
            ),
            intent=intent,
        )

    def get_history_turns(self, session_id: str) -> List[ConversationTurn]:
        return self._conversation_repository.get_conversation_turns_by_id(session_id)

    async def save(self, turn: ConversationTurn) -> None:
        self._conversation_repository.add_conversation_turn(conversation_turn=turn)
