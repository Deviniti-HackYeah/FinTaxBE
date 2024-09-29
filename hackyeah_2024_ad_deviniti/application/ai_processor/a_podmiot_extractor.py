import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o_mini


class PodmiotExtractorResult(BaseModel):
    podmiot: Optional[str]


SYSTEM = """
Użytkownik ma odpowiedzieć na pytanie:

Który podmiot składa deklarację podatkową (wybierz wartość od 1 do 5)?
1. Podmiot zobowiązany solidarnie do zapłaty podatku (gdy występuje więcej niż jeden nabywca, np. współwłaściciele samochodu)  
2. Strony umowy zamiany  
3. Wspólnik spółki cywilnej  
4. Pożyczkobiorca, który otrzymał pożyczkę od osoby najbliższej i chce skorzystać ze zwolnienia od podatku  
5. Inny podmiot, który jest jedynym kupującym lub składa oświadczenie o ustanowieniu hipoteki na swojej nieruchomości  

Masz przeanalizować jego odpowiedź i wybrać odpowiednią wartość od 1-5 (musi być numerek). 
Jeśli nie podał wartości to podaj numer null.
"""


class PodmiotExtractor:
    async def call(self, message: str) -> PodmiotExtractorResult:
        llm = get_azure_gpt_4o_mini()
        start = datetime.datetime.now()
        response: PodmiotExtractorResult = await llm.with_structured_output(  # type: ignore
            PodmiotExtractorResult
        ).ainvoke(
            [
                SystemMessage(content=SYSTEM),
                HumanMessage(content=message),
            ]
        )
        end = datetime.datetime.now()
        logger.info(response)
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response
