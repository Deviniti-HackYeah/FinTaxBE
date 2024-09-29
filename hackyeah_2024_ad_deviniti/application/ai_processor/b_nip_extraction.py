import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o_mini


class NipResult(BaseModel):
    nip: Optional[str]


SYSTEM = """
Z podanego pola wyekstrahuj NIP. Jeśli nie będzie poprawny albo nie zostanie podany zwróć null
"""


class NipExtractor:
    async def call(
            self,
            message: str
    ) -> NipResult:
        llm = get_azure_gpt_4o_mini()
        start = datetime.datetime.now()
        response: IsContinuousConversationResult = await llm.with_structured_output(  # type: ignore
            NipResult
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
