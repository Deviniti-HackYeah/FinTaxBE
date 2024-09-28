from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from hackyeah_2024_ad_deviniti.pcc_renderer.PccRenderer import PccRenderer
from fastapi.responses import HTMLResponse, Response

from hackyeah_2024_ad_deviniti.application.ai_processor.situation_verificator import SituationVerification
from hackyeah_2024_ad_deviniti.presentation.dto import (
    QuestionResponseDto,
    Status,
    TextResponses, QuestionRequestDto,
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
async def chat_interaction(session_id: str, request_body: QuestionRequestDto) -> QuestionResponseDto:
    logger.info(f'request with {request_body}')
    process_result = await (SituationVerification().call_azure(request_body.data))
    response_start = 'Twoje zapytanie dotyczy wniosku PCC-3' if process_result.is_ok \
        else 'Twoje zapytanie dotyczy wniosku PCC-3'
    response = f'{response_start}\n\n{process_result.justification}'
    return QuestionResponseDto(
        response=TextResponses(
            agent_1=response,
            agent_2=response,
        ),
        sources=[],
        extras=None,
    )


@app.get("/question/{session_id}")
async def chat_interaction_sample(session_id: str) -> QuestionResponseDto:
    return QuestionResponseDto(
        response=TextResponses(
            agent_1=f"Odpowiedź agent 1 /-/ {session_id}",
            agent_2=f"Odpowiedź agent 2 /-/ {session_id}",
        ),
        sources=[],
        extras=None,
    )

@app.get("/pcc3.html", response_class=HTMLResponse)
async def pcc3(data: str, kod_urzedu: str, pesel: str) -> str:
    renderer = PccRenderer()
    return renderer.render(data, kod_urzedu, pesel)


@app.get("/pcc3.xml")
async def pcc3(data: str, kod_urzedu: str, pesel: str) -> Response:
    renderer = PccRenderer()
    xml = renderer.xml(data, kod_urzedu, pesel)
    return Response(content=xml, media_type="application/xml")
