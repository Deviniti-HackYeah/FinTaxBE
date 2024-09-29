import uuid
from typing import List

from hackyeah_2024_ad_deviniti.application.ai_processor.d_czynnosc_cywilno_prawna import (
    CzynnoscCywilnoPrawnaExtractor,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.d_kwota import KwotaExtractor
from hackyeah_2024_ad_deviniti.application.form_flow.form_step import DialogStep
from hackyeah_2024_ad_deviniti.application.intents import (
    CZYNNOSC_CYWILNO_PRAWNA,
    FINISH,
    POUCZENIE,
    POZYCZKA_KWOTA,
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


class SprzedarzPodstStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == SPRZEDAZ_KWOTA

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await KwotaExtractor().call(user_action.value)
        if result.kwota is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1="Podaj kwote sprzedarzy"),
                ),
                intent=CZYNNOSC_CYWILNO_PRAWNA,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.umowa_pozyczki_podstawa.value = result.kwota
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1="Zaakceptuj pouczenie prawne"),
                ),
                intent=POUCZENIE,
                pcc_3_form=form,
            )


class PozyczkaPodstawaStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == POZYCZKA_KWOTA

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await KwotaExtractor().call(user_action.value)
        if result.kwota is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1="Podaj kwote pozyczki"),
                ),
                intent=POZYCZKA_KWOTA,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.umowa_pozyczki_podstawa.value = result.kwota
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1="Zaakceptuj pouczenie prawne"),
                ),
                intent=POUCZENIE,
                pcc_3_form=form,
            )


class PouczenieStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == POUCZENIE

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await KwotaExtractor().call(user_action.value)
        if result.kwota is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1="Musisz pouczenie zgodę przed wysłaniem"
                    ),
                ),
                intent=POUCZENIE,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.umowa_pozyczki_podstawa.value = result.kwota
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1="Dziekujemy"),
                ),
                intent=FINISH,
                pcc_3_form=form,
            )


class FinishStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == FINISH

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        return TurnResult(
            full_response=TurnResponseFullDto(
                response_id=str(uuid.uuid1()),
                response=TextResponses(agent_1="Dziękujemy"),
            ),
            intent=FINISH,
            pcc_3_form=previous_turns[-1].pcc_3_form,
        )
