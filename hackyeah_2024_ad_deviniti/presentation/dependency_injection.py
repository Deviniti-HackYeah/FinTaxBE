from fastapi import Depends
from sqlmodel import Session

from hackyeah_2024_ad_deviniti.application.conversation_service import (
    ConversationService,
)
from hackyeah_2024_ad_deviniti.config.database import get_database_session
from hackyeah_2024_ad_deviniti.infrastructure.database.repository import (
    ConversationTurnRepository,
)


def get_turn_repository(
    session: Session = Depends(get_database_session),
) -> ConversationTurnRepository:
    return ConversationTurnRepository(session)


def get_conversation_service(
    repository: ConversationTurnRepository = Depends(get_turn_repository),
) -> ConversationService:
    return ConversationService(repository)
