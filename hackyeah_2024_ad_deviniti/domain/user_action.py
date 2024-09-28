from pydantic import BaseModel


class UserAction(BaseModel):
    type: str
    value: str
