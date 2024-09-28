from fastapi import FastAPI

from hackyeah_2024_ad_deviniti.presentation.dto import Status

app = FastAPI()


@app.get("/")
async def root() -> Status:
    return Status(status="ok")
