import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o


class PrzedmiotOpodatkowaniaResult(BaseModel):
    przedmiot_opodatkowania: str


SYSTEM = """
Masz wyciągnąć przedmiot opodatkowania, jeśli nie znajdujesz żadnego to zwróć null
umowa | zmiana umowy | orzeczenie sądu lub ugoda | inne
"""


class PrzedmiotOpodatkowaniaExtractor:
    async def call(
        self,
        message: str,
    ) -> PrzedmiotOpodatkowaniaResult:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: PrzedmiotOpodatkowaniaResult = await llm.with_structured_output(  # type: ignore
            PrzedmiotOpodatkowaniaResult
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
