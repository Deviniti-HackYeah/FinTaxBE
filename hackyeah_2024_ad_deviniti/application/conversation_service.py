import datetime
import uuid
from typing import List

from loguru import logger

from hackyeah_2024_ad_deviniti.application.ai_processor.situation_verificator import (
    SituationVerification,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.yes_no_answer_exract import (
    YesNoQuestionAnswerProcesor,
)
from hackyeah_2024_ad_deviniti.application.form_fill_process import call_for_fill
from hackyeah_2024_ad_deviniti.application.intents import (
    A_ASK_FOR_PCC_DATE,
    ASK_FOR_FILL_PCC3,
    INCORRECT_SITUATION,
    SITUATION_ADDITIONAL_QUESTION,
)
from hackyeah_2024_ad_deviniti.domain.conversation_turn import (
    ConversationTurn,
    TurnResult,
)
from hackyeah_2024_ad_deviniti.domain.pcc_3_form import Pcc3Form
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
            pcc_3_form=Pcc3Form(),
        )
        self._conversation_repository.add_conversation_turn(turn)
        logger.info(f"requested intent {turn_result.intent}")
        return turn

    async def process_for_response(
            self, session_id: str, action: UserAction
    ) -> TurnResult:
        history = self.get_history_turns(session_id)
        # logger.info(history)
        last_intent = history[-1].requested_intent if history else None
        logger.info(f"last_intent: {last_intent}")
        if len(history) == 0 or (
                last_intent
                and last_intent in [SITUATION_ADDITIONAL_QUESTION, INCORRECT_SITUATION]
        ):
            return await self.process_situation_verification(action, history)
        elif last_intent == ASK_FOR_FILL_PCC3:
            return await self.process_ask_to_start(action)
        else:
            return await call_for_fill(action, history)

    async def process_situation_verification(
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
            ASK_FOR_FILL_PCC3
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
                response_id=str(uuid.uuid1()),
                response=TextResponses(
                    agent_1=response,
                    agent_2=(
                        "Dołączam dokument który pokazuje wniosek PCC-3, czy chcesz go wypełnić?"
                        if ASK_FOR_FILL_PCC3 == intent
                        else ""
                    ),
                ),
                sources=[],
                extras=(
                    [
                        QuestionExtrasDocument(
                            type="document",
                            payload=DocumentPayload(
                                title="pcc-3.pdf",
                                url="https://www.podatki.gov.pl/media/4135/pcc-3-05-012.pdf",
                            ),
                        )
                    ]
                    if ASK_FOR_FILL_PCC3 == intent
                    else []
                ),
            ),
            intent=intent,
            pcc_3_form=Pcc3Form(),
        )

    async def process_ask_to_start(self, action: UserAction) -> TurnResult:
        process_result = await YesNoQuestionAnswerProcesor().call(action.value)
        response_message = (
            "Kiedy miało miejsce zawarcie umowy cywilno prawnej?"
            if process_result.is_yes()
            else (
                "Rozumiem, czy mogę Ci jeszcze w czymś pomóc?"
                if process_result.is_no()
                else "Proszę odpowiedz na pytanie czy chcesz wypełnić formularz PCC-3?"
            )
        )
        intent = (
            A_ASK_FOR_PCC_DATE
            if process_result.is_yes()
            else (
                SITUATION_ADDITIONAL_QUESTION
                if process_result.is_no()
                else ASK_FOR_FILL_PCC3
            )
        )
        return TurnResult(
            full_response=TurnResponseFullDto(
                response_id=str(uuid.uuid1()),
                response=TextResponses(agent_1=response_message, agent_2=""),
                sources=[],
                extras=[],
            ),
            intent=intent,
            pcc_3_form=Pcc3Form(),
        )

    def get_history_turns(self, session_id: str) -> List[ConversationTurn]:
        return self._conversation_repository.get_conversation_turns_by_id(session_id)

    async def save(self, turn: ConversationTurn) -> None:
        self._conversation_repository.add_conversation_turn(conversation_turn=turn)
