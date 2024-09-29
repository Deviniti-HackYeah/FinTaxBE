from typing import List

from loguru import logger
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from hackyeah_2024_ad_deviniti.domain.conversation_turn import ConversationTurn
from hackyeah_2024_ad_deviniti.infrastructure.database.db_model import (
    ConversationTurnDB,
)
from hackyeah_2024_ad_deviniti.infrastructure.database.mappers import (
    map_pydantic_to_sqlalchemy,
    map_sqlalchemy_to_pydantic,
)


class ConversationTurnRepository:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def add_conversation_turn(self, conversation_turn: ConversationTurn) -> None:
        self._session.add(map_pydantic_to_sqlalchemy(conversation_turn))
        self._session.commit()

    def get_conversation_turns_by_id(self, session_id: str) -> List[ConversationTurn]:
        logger.info(f"search {session_id}")
        stmt = select(ConversationTurnDB).where(
            ConversationTurnDB.session_id == session_id
        )
        return sorted(
            [
                map_sqlalchemy_to_pydantic(it)
                for it in self._session.execute(stmt).scalars().all()
            ],
            key=lambda x: x.requested_at,
        )
