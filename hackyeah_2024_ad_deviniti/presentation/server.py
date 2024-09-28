from fastapi import FastAPI

from hackyeah_2024_ad_deviniti.presentation.dto import (
    QuestionResponseDto,
    Status,
    TextResponses,
)

app = FastAPI()


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
