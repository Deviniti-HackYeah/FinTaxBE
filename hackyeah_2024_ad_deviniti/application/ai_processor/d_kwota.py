import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o


class KwotaResponse(BaseModel):
    kwota: Optional[str]


SYSTEM = """
Masz ekstrachować kwoty które są pozytywne, jeśli nie to zwróć Null
"""


class KwotaExtractor:
    async def call(
            self,
            message: str,
    ) -> KwotaResponse:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: KwotaResponse = await llm.with_structured_output(  # type: ignore
            KwotaResponse
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
