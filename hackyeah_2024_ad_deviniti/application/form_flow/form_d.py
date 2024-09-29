import uuid
from typing import List

from hackyeah_2024_ad_deviniti.application.ai_processor.c_przedmiot_opodatkowania_extractor import (
    PrzedmiotOpodatkowaniaExtractor,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.d_czynnosc_cywilno_prawna import (
    CzynnoscCywilnoPrawnaExtractor,
)
from hackyeah_2024_ad_deviniti.application.form_flow.form_step import DialogStep
from hackyeah_2024_ad_deviniti.application.intents import (
    CZYNNOSC_CYWILNO_PRAWNA,
    OKRESLENIE_TRESCI,
    POZYCZKA_KWOTA,
    RODZAJ_PODATNIKA,
    SPRZEDAZ_KWOTA,
)
from hackyeah_2024_ad_deviniti.domain.conversation_turn import (
    ConversationTurn,
    TurnResult,
)
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.presentation.dto import (
    TextResponses,
    TurnResponseFullDto,
)


class CzynnoscCywilnoPrawnaStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == CZYNNOSC_CYWILNO_PRAWNA

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await CzynnoscCywilnoPrawnaExtractor().call(user_action.value)
        if result.czynnosc_cywilno_prawna is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1="Podaj przedmiot opodatkowania"),
                ),
                intent=CZYNNOSC_CYWILNO_PRAWNA,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.rodzaj_czynnosci_cywilno_prawnej.value = result.czynnosc_cywilno_prawna
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1="Podaj zwięzłe określenie treści"),
                ),
                intent=(
                    SPRZEDAZ_KWOTA
                    if result.czynnosc_cywilno_prawna == "SPRZEDAZ"
                    else POZYCZKA_KWOTA
                ),
                pcc_3_form=form,
            )
