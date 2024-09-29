import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import (
    get_azure_gpt_4o,
    get_azure_gpt_4o_mini,
)


class AddressResult(BaseModel):
    kraj: str
    miejscowosc: str
    kod_pocztowy: str
    ulica: Optional[str]
    numer_domu: str
    numer_lokalu: Optional[str]
    powiat: Optional[str]
    gmina: Optional[str]
    not_address: bool


SYSTEM = """
Jesteś przygotowującym adresy w systemie wypełniającym formularze.
Twoim zadaniem jest podać:
 - kraj
 - miejscowość
 - kod pocztowy
 - ulicę
 - numer domu
 - numer mieszkania
 - powiat
 - gmina
 
 Jeśli nie został podany adres, albo nie dało się go wypełnić to not_address=True
 W przypadku adresów zagranicznych, adresów bez ulic itp.. nie podawaj tych wartości.
 """


class AdresExtractor:
    async def call(
        self,
        message: str,
    ) -> AddressResult:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: AddressResult = await llm.with_structured_output(  # type: ignore
            AddressResult
        ).ainvoke(
            [
                SystemMessage(content=SYSTEM),
                HumanMessage(content=f"{message}"),
            ]
        )
        end = datetime.datetime.now()
        logger.info(response)
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response
