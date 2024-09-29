import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o_mini


class IdentyfikatorPodatkowyResult(BaseModel):
    identyfikator_podatkowy_wartosc: Optional[str]


SYSTEM = """
Twoim zadaniem jest wyekstrahować identyfikator podatkowy.
Jeśli będzie niepoprawny to zwróć null.
"""


class IdentyfikatorPodatkowyExtractor:
    async def call(
            self,
            message: str,
            type: str
    ) -> IdentyfikatorPodatkowyResult:
        llm = get_azure_gpt_4o_mini()
        start = datetime.datetime.now()
        response: IsContinuousConversationResult = await llm.with_structured_output(  # type: ignore
            IdentyfikatorPodatkowyResult
        ).ainvoke(
            [
                SystemMessage(content=SYSTEM),
                HumanMessage(content=f'wyciągnij {type}:\n\n{message}'),
            ]
        )
        end = datetime.datetime.now()
        logger.info(response)
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response
