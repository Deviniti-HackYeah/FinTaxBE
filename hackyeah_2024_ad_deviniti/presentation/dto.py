from typing import List, Literal, Optional, Union

from pydantic import BaseModel


class Status(BaseModel):
    status: str


class QuestionSource(BaseModel):
    description: str
    title: str
    url: str


class QuestionExtrasDocument(BaseModel):
    type: Literal["document"]
    payload: dict


class QuestionExtrasImage(BaseModel):
    type: Literal["image"]
    payload: dict


class QuestionExtrasQuote(BaseModel):
    type: Literal["quote"]
    payload: dict


class QuestionExtrasLink(BaseModel):
    type: Literal["link"]
    payload: dict


QuestionExtras = Union[
    QuestionExtrasDocument,
    QuestionExtrasImage,
    QuestionExtrasQuote,
    QuestionExtrasLink,
]


class QuestionRequestDto(BaseModel):
    data: str


class TextResponses(BaseModel):
    agent_1: str
    agent_2: str


class QuestionResponseDto(BaseModel):
    response: TextResponses
    sources: List[QuestionSource]
    extras: Optional[QuestionExtras]
