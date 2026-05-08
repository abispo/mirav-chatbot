from app.schemas.events import EventBody
from app.schemas.actions import ActionPayload, Action, ActionContent
from app.services.llm import generate_response
from app.services.webhook import send_actions
from app.core.logging import logger


def process_event(event: EventBody) -> None:
    try:
        logger.info(f"Processando evento {event.event_id}")

        llm_response = generate_response(event.message.text)

        payload = ActionPayload(
            actions=[
                Action(
                    action="send_message",
                    channel=event.channel,
                    conversation_id=event.conversation.id,
                    content=ActionContent(
                        type="text",
                        text=llm_response,
                    ),
                )
            ]
        )

        send_actions(payload.model_dump())

    except Exception as e:
        logger.error(f"Erro ao processar evento {event.event_id}: {e}")
