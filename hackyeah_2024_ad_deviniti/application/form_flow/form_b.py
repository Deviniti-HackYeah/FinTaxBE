import uuid
from typing import List

from hackyeah_2024_ad_deviniti.application.ai_processor.b_address_extraction import (
    AdresExtractor,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.b_address_verification_extraction import (
    AdresVerifyExtractor,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.b_identyfikator_podatkowy_extract import (
    IdentyfikatorPodatkowyExtractor,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.b_identyfikator_podatkowy_wartosc_extract import (
    IdentyfikatorPodatkowyWartoscExtractor,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.b_nip_extraction import (
    NipExtractor,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.b_rodzaj_podatnika import (
    RodzajPodatnikaExtractor,
)
from hackyeah_2024_ad_deviniti.application.ai_processor.b_urzad_skarbowy_extraction_extraction import (
    UsExtractor,
)
from hackyeah_2024_ad_deviniti.application.form_flow.form_step import DialogStep
from hackyeah_2024_ad_deviniti.application.intents import (
    ADDRESS,
    IDENTYFIKATOR_PODATKOWY,
    IDENTYFIKATOR_PODATKOWY_WARTOSC,
    NIP,
    PRZEDMIOT_OPODATKOWANIA,
    RODZAJ_PODATNIKA,
    URZAD_SKARBOWY_VERIFY,
    VERIFY_ADDRESS,
)
from hackyeah_2024_ad_deviniti.domain.conversation_turn import (
    ConversationTurn,
    TurnResult,
)
from hackyeah_2024_ad_deviniti.domain.pcc_3_form import Pcc3Form
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.presentation.dto import (
    TextResponses,
    TurnResponseFullDto,
)
from hackyeah_2024_ad_deviniti.tools import require_value


class RodzajPodatnikaStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == RODZAJ_PODATNIKA

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await RodzajPodatnikaExtractor().call(user_action.value)
        if result.podatnik is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1="Niestety nie podałeś właściwej daty zawarcia umowy cywilno prawnej, "
                        "musisz podać dzień i miesiąc oraz rok jeśli nie był to bieżący rok."
                    ),
                ),
                intent=RODZAJ_PODATNIKA,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.rodzaj_podatnika.value = result.podatnik
            if result.podatnik == "NIE_FIZYCZNA":
                intent = NIP
                message = "Podaj NIP"
            else:
                intent = IDENTYFIKATOR_PODATKOWY
                message = "Podaj swój identyfikator podatkowy, możesz wybrać pomiędzy NIP i PESEL"
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1=message),
                ),
                intent=intent,
                pcc_3_form=form,
            )


class NipStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == NIP

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await NipExtractor().call(user_action.value)
        if result.nip is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1="Niestety nie podałeś właściwej daty zawarcia umowy cywilno prawnej, "
                        "musisz podać dzień i miesiąc oraz rok jeśli nie był to bieżący rok."
                    ),
                ),
                intent=NIP,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.nip.value = result.nip
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1=f"Dziękuję, proszę podaj teraz Adres (miejscowośc, ulicę oraz nummer domu/mieszkania)"
                    ),
                ),
                intent=ADDRESS,
                pcc_3_form=form,
            )


class IdentyfikatorPodatkowyStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == IDENTYFIKATOR_PODATKOWY

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await IdentyfikatorPodatkowyExtractor().call(user_action.value)
        if result.identyfikator_podatkowy is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1="Proszę o wybór pomiędzy PESEL i NIP."
                    ),
                ),
                intent=IDENTYFIKATOR_PODATKOWY,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.identyfikator_podatkowy.value = result.identyfikator_podatkowy
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1=f"Super, to podaj teraz {result.identyfikator_podatkowy}"
                    ),
                ),
                intent=IDENTYFIKATOR_PODATKOWY_WARTOSC,
                pcc_3_form=form,
            )


class IdentyfikatorPodatkowyWartoscStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == IDENTYFIKATOR_PODATKOWY_WARTOSC

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        identyfikator_podatkowy_typ = previous_turns[
            -1
        ].pcc_3_form.identyfikator_podatkowy
        result = await IdentyfikatorPodatkowyWartoscExtractor().call(
            user_action.value, require_value(identyfikator_podatkowy_typ.value)
        )
        if result.identyfikator_podatkowy_wartosc is None:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1=f"Proszę podać poprawny {identyfikator_podatkowy_typ}"
                    ),
                ),
                intent=IDENTYFIKATOR_PODATKOWY_WARTOSC,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.identyfikator_podatkowy_wartosc.value = (
                result.identyfikator_podatkowy_wartosc
            )
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1=f"Dziękuję, proszę podaj teraz Adres (miejscowośc, ulicę oraz nummer domu/mieszkania)"
                    ),
                ),
                intent=ADDRESS,
                pcc_3_form=form,
            )


class AddressStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == ADDRESS

    def build_result_message_for_verify(self, pcc_3_form: Pcc3Form) -> str:
        results = []
        if pcc_3_form.kraj:
            results.append(f"kraj: {pcc_3_form.kraj}")
        if pcc_3_form.wojwodztwo:
            results.append(f"wojwodztwo: {pcc_3_form.wojwodztwo}")
        if pcc_3_form.powiat:
            results.append(f"powiat: {pcc_3_form.powiat}")
        if pcc_3_form.gmina:
            results.append(f"gmina: {pcc_3_form.gmina}")
        if pcc_3_form.kod_pocztowy:
            results.append(f"kod pocztowy: {pcc_3_form.kod_pocztowy}")
        merged = ", ".join(results)
        return (
            f"Podczas weryfikowania formularze znalazłem następujące dane: {merged} – jeśli jakakolwiek informacja "
            f"jest niepoprawna proszę podać poprawną wartość, w przeciwnym wypadku proszę napisać OK"
        )

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await AdresExtractor().call(user_action.value)
        if result.not_address:
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(agent_1=f"Proszę podać adres jeszcze raz"),
                ),
                intent=ADDRESS,
                pcc_3_form=previous_turns[-1].pcc_3_form,
            )
        else:
            form = previous_turns[-1].pcc_3_form
            form.kraj.value = result.kraj
            form.miejscowosc.value = result.miejscowosc
            form.ulica.value = result.ulica
            form.numer_domu.value = result.numer_domu
            form.kod_pocztowy.value = result.kod_pocztowy
            form.gmina.value = result.gmina
            form.powiat.value = result.powiat
            return TurnResult(
                full_response=TurnResponseFullDto(
                    response_id=str(uuid.uuid1()),
                    response=TextResponses(
                        agent_1=self.build_result_message_for_verify(form)
                    ),
                ),
                intent=VERIFY_ADDRESS,
                pcc_3_form=form,
            )


class AddressVerifyStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == VERIFY_ADDRESS

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        result = await AdresVerifyExtractor().call(user_action.value)

        form = previous_turns[-1].pcc_3_form
        if result.kraj:
            form.kraj.value = result.kraj
        if result.kod_pocztowy:
            form.kod_pocztowy.value = result.kod_pocztowy
        if result.powiat:
            form.powiat.value = result.powiat
        if result.gmina:
            form.gmina.value = result.gmina
        if result.kraj == "Polska":
            result_us = await UsExtractor().call(
                f"{form.ulica.value} {form.numer_domu.value} {form.miejscowosc.value} {form.kod_pocztowy.value}"
            )
            form.urzad_skarbowy.value = result_us.us_kod
            intent = URZAD_SKARBOWY_VERIFY
            message = (
                "Na podstawie adresu wyszukałem Twój Urząd Skarbowy, proszę zweryfikuj czy poprawny. "
                "Jeśli nie podaj właściwy."
            )
        else:
            intent = PRZEDMIOT_OPODATKOWANIA
            message = "Podaj przedmiot opodatkowania"
        return TurnResult(
            full_response=TurnResponseFullDto(
                response_id=str(uuid.uuid1()),
                response=TextResponses(agent_1=message),
            ),
            intent=intent,
            pcc_3_form=form,
        )


class UrzadSkarbowyStep(DialogStep):

    def choose_this_step(
        self, previous_turns: List[ConversationTurn], user_action: UserAction
    ) -> bool:
        return previous_turns[-1].requested_intent == URZAD_SKARBOWY_VERIFY

    async def process_step(
        self, user_action: UserAction, previous_turns: List[ConversationTurn]
    ) -> TurnResult:
        form = previous_turns[-1].pcc_3_form
        result = (await UsExtractor().call(user_action.value)).us_kod
        if result:
            form.urzad_skarbowy.value = result
        return TurnResult(
            full_response=TurnResponseFullDto(
                response_id=str(uuid.uuid1()),
                response=TextResponses(agent_1="Podaj przedmiot opodatkowania"),
            ),
            intent=PRZEDMIOT_OPODATKOWANIA,
            pcc_3_form=form,
        )
