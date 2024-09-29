from typing import List

from hackyeah_2024_ad_deviniti.application.ai_processor.a_cel_deklaracji_extractor import CelDeklaracjiExtractor
from hackyeah_2024_ad_deviniti.application.ai_processor.a_date_extractor import DateExtractor
from hackyeah_2024_ad_deviniti.application.ai_processor.a_podmiot_extractor import PodmiotExtractor
from hackyeah_2024_ad_deviniti.application.form_flow.form_step import DialogStep
from hackyeah_2024_ad_deviniti.application.intents import A_ASK_FOR_PCC_DATE, CEL_ZLOZENIA_DEKLARACJI, \
    PODMIOT_SKLADAJACY, RODZAJ_PODATNIKA
from hackyeah_2024_ad_deviniti.domain.conversation_turn import ConversationTurn, TurnResult
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.presentation.dto import TurnResponseFullDto, TextResponses

PODMIOT_QUESTION = """
Który podmiot składa deklarację podatkową (wybierz wartość od 1 do 5)?

1. Podmiot zobowiązany solidarnie do zapłaty podatku (gdy występuje więcej niż jeden nabywca, np. współwłaściciele samochodu)  
2. Strony umowy zamiany  
3. Wspólnik spółki cywilnej  
4. Pożyczkobiorca, który otrzymał pożyczkę od osoby najbliższej i chce skorzystać ze zwolnienia od podatku  
5. Inny podmiot, który jest jedynym kupującym lub składa oświadczenie o ustanowieniu hipoteki na swojej nieruchomości  
"""

RODZAJ_PODATNIKA_QUESTION = """
Jaki jest rodzaj podatnika składającego deklarację? (osoba fizyczna, albo osoba niefizyczna)
"""


class DateStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == A_ASK_FOR_PCC_DATE

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        result = await DateExtractor().call(user_action.value)
        if result.date_str is None:
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
            form.dzien_dokonania.value = result.date_str
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


class CelZlozeniaStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == CEL_ZLOZENIA_DEKLARACJI

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        result = await CelDeklaracjiExtractor().call(user_action.value)
        if result.cel_deklaracji is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1=("Masz dwie opcje do wyboru. Jeśli składasz deklarację po raz pierwszy, "
                                 "wybierasz złożenie. Jeśli poprawiasz wcześniej złożony dokument, wybierasz korektę. "
                                 "Nie da się tu nic więcej dopowiedzieć.")
                    ),
                    sources=[],
                    extras=[]
                ),
                intent=CEL_ZLOZENIA_DEKLARACJI,
                pcc_3_form=previous_turns[-1].pcc_3_form
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.dzien_dokonania.value = result.cel_deklaracji
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1=PODMIOT_QUESTION),
                    sources=[],
                    extras=[]
                ),
                intent=PODMIOT_SKLADAJACY,
                pcc_3_form=form
            )


class PodmiotSkladajacyjStep(DialogStep):

    def choose_this_step(self, previous_turns: List[ConversationTurn], user_action: UserAction) -> bool:
        return previous_turns[-1].requested_intent == PODMIOT_SKLADAJACY

    async def process_step(self, user_action: UserAction,
                           previous_turns: List[ConversationTurn]) -> TurnResult:
        result = await PodmiotExtractor().call(user_action.value)
        if result.podmiot is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1="Niestety nie podałeś właściwej daty zawarcia umowy cywilno prawnej, "
                                "musisz podać dzień i miesiąc oraz rok jeśli nie był to bieżący rok."
                    ),
                    sources=[],
                    extras=[]
                ),
                intent=PODMIOT_SKLADAJACY
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.dzien_dokonania.value = result.podmiot
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response=TextResponses(
                        agent_1=RODZAJ_PODATNIKA_QUESTION),
                    sources=[],
                    extras=[]
                ),
                intent=RODZAJ_PODATNIKA,
                pcc_3_form=form
            )
