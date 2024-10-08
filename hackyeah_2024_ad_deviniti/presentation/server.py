from typing import Any, List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from loguru import logger
from hackyeah_2024_ad_deviniti.infrastructure.llm_loaders import (
    get_azure_gpt_4o,
    get_azure_gpt_4o_mini,
)
from langchain_core.messages import HumanMessage, SystemMessage



from hackyeah_2024_ad_deviniti.application.conversation_service import (
    ConversationService,
)
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.pcc_renderer.PccRenderer import PccRenderer
from hackyeah_2024_ad_deviniti.presentation.dependency_injection import (
    get_conversation_service,
)
from hackyeah_2024_ad_deviniti.presentation.dto import (
    QuestionRequestDto,
    Status,
    TurnResponseFullDto,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Status:
    return Status(status="ok")


@app.post("/question/{session_id}")
async def chat_interaction(
        session_id: str,
        request_body: QuestionRequestDto,
        service: ConversationService = Depends(get_conversation_service),
) -> TurnResponseFullDto:
    logger.info(f"request with {request_body}")
    user_action = UserAction(type="message", value=request_body.data)
    turn = await service.run_turn(session_id, user_action)
    return turn.full_response


@app.get("/history/{session_id}")
async def history(
        session_id: str,
        service: ConversationService = Depends(get_conversation_service),
) -> List[Any]:
    turns = service.get_history_turns(session_id)
    to_return: List[Any] = []
    for it in turns:
        to_return.append({"data": it.user_action.value})
        to_return.append(it.full_response)
    return to_return


@app.get("/pcc3.html", response_class=HTMLResponse)
async def pcc3_html() -> str:
    renderer = PccRenderer()
    return renderer.render2()


@app.get("/pcc3.xml")
async def pcc3_xml(data: str, kod_urzedu: str, pesel: str) -> Response:
    renderer = PccRenderer()
    xml = renderer.xml(data, kod_urzedu, pesel)
    return Response(content=xml, media_type="application/xml")

@app.get("/xml")
async def pcc3_xml2() -> Response:
    renderer = PccRenderer()
    xml = renderer.xml2()
    return Response(content=xml, media_type="application/xml")



@app.get("/chat")
async def chat(s : str) -> Any:
    gpt = get_azure_gpt_4o()
    x = gpt.invoke([
                SystemMessage(content="Jesteś doradcą podatkowym i udzielasz informacji na temat podatków. Nie rozmawaiasz na innne tematy."),
                HumanMessage(content=s),
            ])
    return x