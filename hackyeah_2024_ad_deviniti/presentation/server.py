import datetime
import uuid

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from loguru import logger

from hackyeah_2024_ad_deviniti.application.ai_processor.situation_verificator import (
    SituationVerification,
)
from hackyeah_2024_ad_deviniti.application.conversation_service import (
    ConversationService,
)
from hackyeah_2024_ad_deviniti.domain.conwersation_turn import ConversationTurn
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.pcc_renderer.PccRenderer import PccRenderer
from hackyeah_2024_ad_deviniti.presentation.dependency_injection import (
    get_conversation_service,
)
from hackyeah_2024_ad_deviniti.presentation.dto import (
    QuestionRequestDto,
    Status,
    TextResponses,
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


@app.get("/pcc3.html", response_class=HTMLResponse)
async def pcc3_html(data: str, kod_urzedu: str, pesel: str) -> str:
    renderer = PccRenderer()
    return renderer.render(data, kod_urzedu, pesel)


@app.get("/pcc3.xml")
async def pcc3_xml(data: str, kod_urzedu: str, pesel: str) -> Response:
    renderer = PccRenderer()
    xml = renderer.xml(data, kod_urzedu, pesel)
    return Response(content=xml, media_type="application/xml")
