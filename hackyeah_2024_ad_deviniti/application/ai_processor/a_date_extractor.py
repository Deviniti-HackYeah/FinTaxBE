import asyncio
import datetime
from typing import List, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.domain.conversation_turn import ConversationTurn
from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import (
    get_azure_gpt_4o,
    get_azure_gpt_4o_mini,
)


class DateExtractorResult(BaseModel):
    date_str: Optional[str]


SYSTEM = """
Wyekstrahuj YYYY-MM-DD z wartości podanej przez użytkownika, jak się nie da, to zwróć null
Jeśli rok nie jest podany to mamy 2024
"""


class DateExtractor:
    async def call(self, message: str) -> DateExtractorResult:
        llm = get_azure_gpt_4o_mini()
        start = datetime.datetime.now()
        response: DateExtractorResult = await llm.with_structured_output(  # type: ignore
            DateExtractorResult
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
