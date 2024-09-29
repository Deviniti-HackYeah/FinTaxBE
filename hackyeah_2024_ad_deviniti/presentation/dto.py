from typing import List, Literal, Optional, Union

from pydantic import BaseModel


class Status(BaseModel):
    status: str


class QuestionSource(BaseModel):
    description: str
    title: str
    url: str


class DocumentPayload(BaseModel):
    title: str
    url: str


class ImagePayload(BaseModel):
    url: str


class QuotePayload(BaseModel):
    text: str


class LinkPayload(BaseModel):
    title: str
    url: str


class QuestionExtrasDocument(BaseModel):
    type: Literal["document"] = "document"
    payload: DocumentPayload


class QuestionExtrasImage(BaseModel):
    type: Literal["image"]
    payload: ImagePayload


class QuestionExtrasQuote(BaseModel):
    type: Literal["quote"]
    payload: QuotePayload


class QuestionExtrasLink(BaseModel):
    type: Literal["link"]
    payload: LinkPayload


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


class TurnResponseFullDto(BaseModel):
    response: TextResponses
    sources: List[QuestionSource]
    extras: Optional[QuestionExtras]
