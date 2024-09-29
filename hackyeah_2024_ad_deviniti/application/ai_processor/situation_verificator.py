import asyncio
import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o

TEST_CASES = [
    {
        "text": "Spółka z ograniczoną odpowiedzialnością, w której jestem wspólnikiem, podjęła decyzję o podwyższeniu kapitału zakładowego. W związku z tym muszę opłacić należny podatek.",
        "is_ok": True,
    },
    {
        "text": "Tomasz zaciągnął kredyt hipoteczny w wysokości 500 000 zł na budowę domu. W związku z ustanowieniem hipoteki na rzecz banku musi zapłacić podatek od ustanowienia zabezpieczenia.",
        "is_ok": True,
    },
    {
        "text": "Pan Kowalski kupił mieszkanie od dewelopera, podpisując wcześniej umowę przedwstępną. Teraz zawarł umowę przeniesienia własności tej nieruchomości, co wymaga opłacenia podatku.",
        "is_ok": True,
    },
    {
        "text": "Siostry Marta i Ewa postanowiły znieść współwłasność po rodzicach. Ewa wypłaciła Marcie 50 000 zł, aby przejąć całość nieruchomości. Marta musi zapłacić podatek od otrzymanej dopłaty.",
        "is_ok": True,
    },
    {
        "text": "Jan zawarł umowę depozytu nieprawidłowego z kolegą, w której przekazał 100 000 zł do przechowania na rok.",
        "is_ok": True,
    },
    {
        "text": "Monika otrzymała w darowiźnie mieszkanie od swojego ojca, które było obciążone kredytem hipotecznym. przyjęła darowiznę z przejęciem długu.",
        "is_ok": True,
    },
    {
        "text": "Marek i Jacek założyli spółkę cywilną i wniesli do niej wkłady o łącznej wartości 50 000 zł. Zawarcie umowy spółki cywilnej podlega podatkowi.",
        "is_ok": True,
    },
    {
        "text": "Pan Jan sprzedał swojemu kuzynowi prawo użytkowania wieczystego gruntu. W związku z tą transakcją musi opłacić podatek od czynności cywilnoprawnych.",
        "is_ok": True,
    },
    {
        "text": "Anna zawarła umowę odpłatnego użytkowania mieszkania z sąsiadem na okres 5 lat.",
        "is_ok": True,
    },
    {
        "text": "Rodzeństwo odziedziczyło po rodzicach dom, a brat postanowił wypłacić siostrze 100 000 zł w ramach działu spadku, aby przejąć całość. Siostra musi złożyć deklarację PCC-3 i zapłacić podatek od otrzymanej dopłaty.",
        "is_ok": True,
    },
    {
        "text": "Michał zamienił swoje mieszkanie w Warszawie na dom na wsi z kolegą. Ponieważ doszło do zamiany rzeczy, obaj muszą złożyć deklarację PCC-3 i zapłacić podatek od wartości zamienianych nieruchomości.",
        "is_ok": True,
    },
    {"text": "Janek kupił używaną lampę za 800 zł od sąsiada.", "is_ok": False},
    {
        "text": "Ania pożyczyła 10 000 zł od swojej mamy na zakup nowego sprzętu AGD.",
        "is_ok": False,
    },
    {
        "text": "Marta, posiadająca orzeczenie o znacznym stopniu niepełnosprawności, kupiła samochód osobowy na własne potrzeby.",
        "is_ok": False,
    },
    {
        "text": "Tomasz wymienił 5 000 zł na euro w kantorze, aby mieć gotówkę na wakacje za granicą.",
        "is_ok": False,
    },
    {
        "text": "Karol sprzedał swoje mieszkanie, a transakcja została przeprowadzona w formie aktu notarialnego. Notariusz pobrał odpowiedni podatek.",
        "is_ok": False,
    },
    {"text": "Tere fere", "is_ok": False},
    {"text": "Gówno w zoo", "is_ok": False},
    {"text": "O kurwa", "is_ok": False},
]


class SituationVerificationResult(BaseModel):
    is_ok: bool
    justification_in_polish: str


SYSTEM = """
Twoim zadaniem jest odpowiedzenie czy użytkownik z potrzebą jaką ma może wypełnić poniższy dokument (PCC-3)
Jeśli ktoś mówi na inny temat to odpowiedź ma być false, jakieś głupie zapytanie itp... True tylko jak przypadek wchodzi w opis, nawet częściowo -- wtedy uzupełnij.

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
        self, message: str = "Jak dojechać do Polski z Czech?"
    ) -> SituationVerificationResult:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: SituationVerificationResult = await llm.with_structured_output(  # type: ignore
            SituationVerificationResult
        ).ainvoke(
            [SystemMessage(content=SYSTEM), HumanMessage(content=message)]
        )
        end = datetime.datetime.now()
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response


async def main() -> None:
    for it in TEST_CASES:
        logger.info(it["text"])
        logger.info(it["is_ok"])
        # logger.info(await SituationVerification().call(it["text"]))
        logger.info("#####################")
        logger.info("#####################")


if __name__ == "__main__":
    asyncio.run(main())
