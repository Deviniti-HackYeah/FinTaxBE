import asyncio
import datetime
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger
from pydantic import BaseModel

from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import get_azure_gpt_4o


class TopicCheckerResult(BaseModel):
    is_ok: bool
    justification_in_polish: Optional[str]


SYSTEM = """
Twoim zadaniem jest weryfikacja czy rozmowa, ostatnie zapytanie jest na temat, albo związane z tematami podatkowymi.
Jeśli będzie nie na temat, to proszę uzasadnij odpowiadając na pytanie "Dlaczego ta wypowiedź jest nie związana z podatkami?",
Jeśli jest true, to justification_in_polish ma być null
"""


class ConversationTopicChecker:
    async def call(
        self, message: str = "Jak dojechać do Polski z Czech?"
    ) -> TopicCheckerResult:
        llm = get_azure_gpt_4o()
        start = datetime.datetime.now()
        response: TopicCheckerResult = await llm.with_structured_output(TopicCheckerResult).ainvoke(  # type: ignore
            [SystemMessage(content=SYSTEM), HumanMessage(content=message)]
        )
        end = datetime.datetime.now()
        logger.info(response)
        logger.info(f"duration: {(end - start).total_seconds()}s")
        return response


async def main() -> None:
    await ConversationTopicChecker().call("Czy jutro będzie padał deszcz?")
    await ConversationTopicChecker().call("Kto wygrał MŚ w świata z piłce nożnej?")
    await ConversationTopicChecker().call("Czy muszę płacić VAT?")
    await ConversationTopicChecker().call("Jak dojadę do dworca w Krakowie?")
    await ConversationTopicChecker().call("Czy zapłacę duży podatek w przyszłym roku?")
    await ConversationTopicChecker().call("Czy żyrafy muszą płacić podatki?")


if __name__ == "__main__":
    asyncio.run(main())
