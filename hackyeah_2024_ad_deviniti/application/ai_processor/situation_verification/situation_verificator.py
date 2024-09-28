from abc import ABC, abstractmethod

from pydantic import BaseModel


class SituationVerificationResult(BaseModel):
    is_ok: bool


class SituationVerification(ABC):
    @abstractmethod
    async def call(self, message: str) -> SituationVerificationResult:
        pass
