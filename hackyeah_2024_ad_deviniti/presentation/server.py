from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hackyeah_2024_ad_deviniti.presentation.dto import (
    QuestionResponseDto,
    Status,
    TextResponses,
)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Status:
    return Status(status="ok")


@app.post("/question/{session_id}")
async def chat_interaction(session_id: str) -> QuestionResponseDto:
    return QuestionResponseDto(
        response=TextResponses(
            agent_1=f"Odpowiedź agent 1 /-/ {session_id}",
            agent_2=f"Odpowiedź agent 2 /-/ {session_id}",
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
