import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o_mini


class RodzajPodatnikaExtractorResult(BaseModel):
    podatnik: Optional[str]


SYSTEM = """
Użytkownik ma odpowiedzieć na pytanie:

Wybierz rodzaj podatnika:
ma do wyboru pomiędzy osobą fizyczną a osobą nie-fizyczną.

Masz zwrócić jedną z Opcji:
 - FIZYCZNA
 - NIE_FIZYCZNA
 - NULL -- jeśli nie da się przypasować.
"""


class RodzajPodatnikaExtractor:
    async def call(
            self,
            message: str
    ) -> RodzajPodatnikaExtractorResult:
        llm = get_azure_gpt_4o_mini()
        start = datetime.datetime.now()
        response: IsContinuousConversationResult = await llm.with_structured_output(  # type: ignore
            RodzajPodatnikaExtractorResult
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
