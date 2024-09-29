from typing import List, Optional

from hackyeah_2024_ad_deviniti.domain.conwersation_turn import ConversationTurn


def get_history_context(
    history: List[ConversationTurn], message: Optional[str] = None
) -> str:
    history_messages: List[str] = []
    for it in history:
        history_messages.append(f"User: {it.user_action.value}")
        history_messages.append(f"Assistant: {it.full_response.response.agent_1}")
    if message:
        history_messages.append(f"User: {message}")
    return "\n\n".join(history_messages)
