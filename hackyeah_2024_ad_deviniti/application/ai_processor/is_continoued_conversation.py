import asyncio
import datetime
from typing import List

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.domain.conwersation_turn import ConversationTurn
from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o


class IsContinuousConversationResult(BaseModel):
    is_ok: bool


SYSTEM = """
Poniżej dostaniesz w chronologicznej kolejności ostatnie wiadomości konwersacji.
Twoim zadaniem jest zweryfikowanie czy jest to kontunowanie konwersacji
"""


class IsContinuousConversationChecker:
    async def call(
        self,
        previous_turns: List[ConversationTurn],
        message: str = "Jak dojechać do Polski z Czech?",
    ) -> IsContinuousConversationResult:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        history_messages: List[str] = []
        for it in previous_turns:
            history_messages.append(f"User: {it.user_action.value}")
            history_messages.append(f"Assistant: {it.full_response.response.agent_1}")
        history_messages.append(f"User: {message}")
        response: IsContinuousConversationResult = await llm.with_structured_output(  # type: ignore
            IsContinuousConversationResult
        ).ainvoke(
            [
                SystemMessage(content=SYSTEM),
                HumanMessage(content="\n\n".join(history_messages)),
            ]
        )
        end = datetime.datetime.now()
        logger.info(response)
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response
