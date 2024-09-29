import datetime
from typing import List, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.application.ai_processor.tools import get_history_context
from hackyeah_2024_ad_deviniti.domain.conversation_turn import ConversationTurn
from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o


class SituationVerificationResult(BaseModel):
    is_ok: bool
    should_ask_additional_question: bool
    justification_in_polish: Optional[str]
    additional_question: Optional[str]


SYSTEM = """
Twoim zadaniem jest odpowiedzenie czy użytkownik z potrzebą jaką ma może wypełnić poniższy dokument (PCC-3)
Jeśli ktoś mówi na inny temat to odpowiedź ma być false, jakieś głupie zapytanie itp...
True tylko jak jesteś pewny że pasuje i argument musi być w 100% zgodny.
Jak odpowiedź wymaga odpowiedzi na dodatkowe pytanie zadaj je i oznacz should_ask_additional_question.


######################

To jest opis do składania deklaracji PCC-3

**Deklarację składa się w przypadku:**

- zawarcia umowy: sprzedaży, zamiany rzeczy i praw majątkowych, pożyczki pieniędzy lub rzeczy oznaczonych tylko co do gatunku (jeśli z góry nie zostanie ustalona suma pożyczki – deklaracje składa się w przypadku każdorazowej wypłaty środków pieniężnych), o dział spadku lub zniesienie współwłasności, gdy dochodzi w nich do spłat i dopłat, ustanowienia odpłatnego użytkowania (w tym nieprawidłowego), depozytu nieprawidłowego lub spółki,
- przyjęcia darowizny z przejęciem długów i ciężarów albo zobowiązania darczyńcy,
- złożenia oświadczenia o ustanowieniu hipoteki lub zawarcia umowy ustanowienia hipoteki,
- uprawomocnia się orzeczenia sądu lub otrzymania wyroku sądu polubownego albo zawarcia ugody w sprawach umów wyżej wymienionych,
- zawarcia umowy przeniesienia własności – jeśli wcześniej podpisana została umowa zobowiązująca do przeniesienia własności, a teraz podpisana została umowa przeniesienia tej własności,
- podwyższenia kapitału w spółce mającej osobowość prawną.

---

**Deklaracji nie składa się, gdy:**

- czynność cywilnoprawna jest dokonywana w formie aktu notarialnego i podatek jest pobierany przez notariusza (płatnika podatku),
- podatnik składa zbiorczą deklarację w sprawie podatku od czynności cywilnoprawnych (PCC-4),
- podatnikiem jest:
    - kupujący na własne potrzeby sprzęt rehabilitacyjny, wózki inwalidzkie, motorowery, motocykle lub samochody osobowe – jeśli ma: orzeczenie o znacznym albo umiarkowanym stopniu niepełnosprawności (nieważne, jakie ma schorzenie), o orzeczenie o lekkim stopniu niepełnosprawności w związku ze schorzeniami narządów ruchu,
    - organizacja pożytku publicznego – jeśli dokonuje czynności cywilnoprawnych tylko w związku ze swoją nieodpłatną działalnością pożytku publicznego,
    - jednostka samorządu terytorialnego,
    - Skarb Państwa,
    - Agencja Rezerw Materiałowych,  
- korzysta się ze zwolnienia od podatku, gdy:
    - kupowane są obce waluty,
    - kupowane są i zamieniane waluty wirtualne,
    - kupowane są rzeczy ruchome – i ich wartość rynkowa nie przekracza 1 000 zł,
    - pożyczane jest nie więcej niż 36 120 zł (liczą się łącznie pożyczki z ostatnich 5 lat od jednej osoby) – jeśli jest to pożyczka od bliskiej rodziny, czyli od: małżonka, dzieci, wnuków, prawnuków, rodziców, dziadków, pradziadków, pasierbów, pasierbic, rodzeństwa, ojczyma, macochy, zięcia, synowej, teściów,
    - pożyczane są pieniądze od osób spoza bliskiej rodziny – jeśli wysokość pożyczki nie przekracza 1 000 zł."""


class SituationVerification:
    async def call(
            self, message: str, history: List[ConversationTurn]
    ) -> SituationVerificationResult:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: SituationVerificationResult = await llm.with_structured_output(  # type: ignore
            SituationVerificationResult
        ).ainvoke(
            [
                SystemMessage(content=SYSTEM),
                HumanMessage(content=get_history_context(history, message)),
            ]
        )
        end = datetime.datetime.now()
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response
