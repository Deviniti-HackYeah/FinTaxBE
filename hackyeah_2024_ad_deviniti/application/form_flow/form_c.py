from typing import List

from hackyeah_2024_ad_deviniti.application.ai_processor.c_przedmiot_opodatkowania_extractor import \
    PrzedmiotOpodatkowaniaExtractor
from hackyeah_2024_ad_deviniti.application.form_flow.form_step import DialogStep
from hackyeah_2024_ad_deviniti.application.intents import RODZAJ_PODATNIKA, \
    OKRESLENIE_TRESCI, CZYNNOSC_CYWILNO_PRAWNA
from hackyeah_2024_ad_deviniti.domain.conversation_turn import ConversationTurn, TurnResult
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.presentation.dto import TurnResponseFullDto, TextResponses


class PrzedmiotOpodatkowaniaStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == RODZAJ_PODATNIKA

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        result = await PrzedmiotOpodatkowaniaExtractor().call(user_action.value)
        if result.przedmiot_opodatkowania is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1="Podaj przedmiot opodatkowania"
                    ),
                ),
                intent=RODZAJ_PODATNIKA,
                pcc_3_form=previous_turns[-1].pcc_3_form
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.przedmiot_opodatkowania.value = result.przedmiot_opodatkowania
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1="Podaj zwięzłe określenie treści"
                    ),
                ),
                intent=OKRESLENIE_TRESCI,
                pcc_3_form=form
            )


class OkreslenieTresciStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == OKRESLENIE_TRESCI

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        form = previous_turns[-1].pcc_3_form
        form.zwiezle_okreslenie_tresci.value = user_action.value
        return TurnResult(
            full_response=TurnResponseFullDto(
                response=TextResponses(
                    agent_1="Podaj zwięzłe określenie treści"
                ),
            ),
            intent=CZYNNOSC_CYWILNO_PRAWNA,
            pcc_3_form=form
        )
