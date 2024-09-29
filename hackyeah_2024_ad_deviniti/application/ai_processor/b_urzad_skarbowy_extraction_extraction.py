import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o


class UsCodeResult(BaseModel):
    us_kod: Optional[str]


SYSTEM = """
Na podstawie podanych danych spróbuj określić kod urzędu skarbowego, 
może być wyrażenie akceptacji -- wtedy nic nie podawaj
 """


class UsExtractor:
    async def call(
            self,
            message: str,
    ) -> UsCodeResult:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: IsContinuousConversationResult = await llm.with_structured_output(  # type: ignore
            UsCodeResult
        ).ainvoke(
            [
                SystemMessage(content=SYSTEM),
                HumanMessage(content=f'{message}'),
            ]
        )
        end = datetime.datetime.now()
        logger.info(response)
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response
