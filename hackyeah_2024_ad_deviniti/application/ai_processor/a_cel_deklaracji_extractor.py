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


class CelDeklaracjiResult(BaseModel):
    cel_deklaracji: Optional[str]


SYSTEM = """
Użytkownik ma odpowiedzieć na pytanie:

Jaki jest cel zlozenia deklaracji. Masz do wyboru 2 opcje: 
*złożenie* jeśli składasz ją po raz pierwszy 
lub *korekta* jeśli chcesz poprawić wcześniej złożony dokument."

Zwróć KOREKTA albo ZLOZENIE
"""


class CelDeklaracjiExtractor:
    async def call(self, message: str) -> CelDeklaracjiResult:
        llm = get_azure_gpt_4o_mini()
        start = datetime.datetime.now()
        response: CelDeklaracjiResult = await llm.with_structured_output(  # type: ignore
            CelDeklaracjiResult
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
