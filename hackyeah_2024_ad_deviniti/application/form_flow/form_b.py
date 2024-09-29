from typing import List

from hackyeah_2024_ad_deviniti.application.ai_processor.b_identyfikator_podatkowy_extract import \
    IdentyfikatorPodatkowyExtractor
from hackyeah_2024_ad_deviniti.application.ai_processor.b_nip_extraction import NipExtractor
from hackyeah_2024_ad_deviniti.application.ai_processor.b_rodzaj_podatnika import RodzajPodatnikaExtractor
from hackyeah_2024_ad_deviniti.application.form_flow.form_step import DialogStep
from hackyeah_2024_ad_deviniti.application.intents import A_ASK_FOR_PCC_DATE, CEL_ZLOZENIA_DEKLARACJI, RODZAJ_PODATNIKA, \
    NIP, IDENTYFIKATOR_PODATKOWY, IDENTYFIKATOR_PODATKOWY_WARTOSC
from hackyeah_2024_ad_deviniti.domain.conversation_turn import ConversationTurn, TurnResult
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.presentation.dto import TurnResponseFullDto, TextResponses


class RodzajPodatnikaStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == RODZAJ_PODATNIKA

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        result = await RodzajPodatnikaExtractor().call(user_action.value)
        if result.podatnik is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1="Niestety nie podałeś właściwej daty zawarcia umowy cywilno prawnej, "
                                "musisz podać dzień i miesiąc oraz rok jeśli nie był to bieżący rok."
                    ),
                ),
                intent=A_ASK_FOR_PCC_DATE,
                pcc_3_form=previous_turns[-1].pcc_3_form
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.rodzaj_podatnika = result.podatnik
            if result.podatnik == 'NIE_FIZYCZNA':
                intent = NIP
                message = "Podaj NIP"
            else:
                intent = IDENTYFIKATOR_PODATKOWY
                message = "Podaj swój identyfikator podatkowy, możesz wybrać pomiędzy NIP i PESEL"
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1=message
                    ),
                ),
                intent=intent,
                pcc_3_form=form
            )


class NipStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == NIP

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        result = await NipExtractor().call(user_action.value)
        if result.nip is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1="Niestety nie podałeś właściwej daty zawarcia umowy cywilno prawnej, "
                                "musisz podać dzień i miesiąc oraz rok jeśli nie był to bieżący rok."
                    ),
                    sources=[],
                    extras=[]
                ),
                intent=A_ASK_FOR_PCC_DATE,
                pcc_3_form=previous_turns[-1].pcc_3_form
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.nip = result.nip
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1="Jaki jest cel zlozenia deklaracji. Masz do wyboru 2 opcje: *złożenie* jeśli "
                                "składasz ją po raz pierwszy lub *korekta* jeśli chcesz poprawić wcześniej złożony "
                                "dokument."),
                    sources=[],
                    extras=[]
                ),
                intent=CEL_ZLOZENIA_DEKLARACJI,
                pcc_3_form=form
            )


class IdentyfikatorPodatkowyStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == IDENTYFIKATOR_PODATKOWY

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        result = await IdentyfikatorPodatkowyExtractor().call(user_action.value)
        if result.identyfikator_podatkowy is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1="Proszę o wybór pomiędzy PESEL i NIP."
                    ),
                    sources=[],
                    extras=[]
                ),
                intent=A_ASK_FOR_PCC_DATE,
                pcc_3_form=previous_turns[-1].pcc_3_form
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.identyfikator_podatkowy = result.identyfikator_podatkowy
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1=f"Super, to podaj teraz {result.identyfikator_podatkowy}"),
                    sources=[],
                    extras=[]
                ),
                intent=IDENTYFIKATOR_PODATKOWY_WARTOSC,
                pcc_3_form=form
            )


class IdentyfikatorPodatkowyWartoscStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == IDENTYFIKATOR_PODATKOWY_WARTOSC

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        result = await IdentyfikatorPodatkowyExtractor().call(user_action.value)
        if result.identyfikator_podatkowy is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1=f"Proszę podać {result.identyfikator_podatkowy}"
                    ),
                    sources=[],
                    extras=[]
                ),
                intent=IDENTYFIKATOR_PODATKOWY_WARTOSC,
                pcc_3_form=previous_turns[-1].pcc_3_form
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.identyfikator_podatkowy = result.identyfikator_podatkowy
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1=f"Super, to podaj teraz {result.identyfikator_podatkowy}"),
                    sources=[],
                    extras=[]
                ),
                intent=IDENTYFIKATOR_PODATKOWY_WARTOSC,
                pcc_3_form=form
            )
