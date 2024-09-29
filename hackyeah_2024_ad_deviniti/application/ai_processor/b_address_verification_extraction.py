import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o_mini, get_azure_gpt_4o


class AddressVerifyResult(BaseModel):
    kraj: Optional[str]
    kod_pocztowy: Optional[str]
    powiat: Optional[str]
    gmina: Optional[str]


SYSTEM = """
W podanym tekście losowo mogą pojawić się kraj, powiat, kod pocztowy, gmina
 """


class AdresVerifyExtractor:
    async def call(
            self,
            message: str,
    ) -> AddressVerifyResult:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: IsContinuousConversationResult = await llm.with_structured_output(  # type: ignore
            AddressVerifyResult
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
