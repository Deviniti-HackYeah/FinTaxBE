from hackyeah_2024_ad_deviniti.domain.conversation_turn import ConversationTurn
from hackyeah_2024_ad_deviniti.domain.pcc_3_form import Pcc3Form
from hackyeah_2024_ad_deviniti.domain.user_action import UserAction
from hackyeah_2024_ad_deviniti.infrastructure.database.db_model import (
    ConversationTurnDB,
)
from hackyeah_2024_ad_deviniti.presentation.dto import TurnResponseFullDto


def map_pydantic_to_sqlalchemy(pydantic_model: ConversationTurn) -> ConversationTurnDB:
    return ConversationTurnDB(
        turn_id=pydantic_model.turn_id,
        session_id=pydantic_model.session_id,
        requested_at=pydantic_model.requested_at,
        returned_at=pydantic_model.returned_at,
        user_action=pydantic_model.user_action.model_dump(),
        full_response=pydantic_model.full_response.model_dump(),
        requested_intent=pydantic_model.requested_intent,
        stats=pydantic_model.stats,
        pcc_3_form=pydantic_model.pcc_3_form.model_dump(),
    )


def map_sqlalchemy_to_pydantic(
        sqlalchemy_model: ConversationTurnDB,
) -> ConversationTurn:
    return ConversationTurn(
        turn_id=sqlalchemy_model.turn_id,
        session_id=sqlalchemy_model.session_id,
        requested_at=sqlalchemy_model.requested_at,
        returned_at=sqlalchemy_model.returned_at,
        user_action=UserAction(**sqlalchemy_model.user_action),
        full_response=TurnResponseFullDto(**sqlalchemy_model.full_response),
        requested_intent=sqlalchemy_model.requested_intent,
        stats=sqlalchemy_model.stats,
        pcc_3_form=Pcc3Form(**sqlalchemy_model.pcc_3_form),
    )
