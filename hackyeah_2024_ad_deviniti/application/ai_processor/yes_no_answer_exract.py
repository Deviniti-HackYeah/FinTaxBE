import asyncio
import datetime
from typing import List, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.application.ai_processor.tools import get_history_context
from hackyeah_2024_ad_deviniti.domain.conversation_turn import ConversationTurn
from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o


class YesNoQuestionResponse(BaseModel):
    question_answer: str

    def is_yes(self) -> bool:
        return self.question_answer.lower() == 'yes'

    def is_no(self) -> bool:
        return self.question_answer.lower() == 'no'

    def is_other(self) -> bool:
        return not self.is_yes() and not self.is_no()


SYSTEM = """
Użytkownik który napisze wiadomość poda swoją odpowiedź na pytanie tak / nie, 
Twoim zadaniem jest ekstrakcja takiej odpowiedzi do wartość TAK, NIE, INNA.
Inna w przypadku kiedy odpowiedź jest trudna do określenia albo nie nawiązuje do zadanego pytania
"""


class YesNoQuestionAnswerProcesor:
    async def call(
            self, message: str
    ) -> YesNoQuestionResponse:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: SituationVerificationResult = await llm.with_structured_output(  # type: ignore
            YesNoQuestionResponse
        ).ainvoke(
            [
                SystemMessage(content=SYSTEM),
                HumanMessage(content=message),
            ]
        )
        end = datetime.datetime.now()
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response
