import httpx
from app.core.config import settings
from app.core.logging import logger


def send_actions(payload: dict) -> None:
    try:
        response = httpx.post(
            settings.N8N_WEBHOOK_URL,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        logger.info("Ações enviadas para o webhook do N8N")
    except httpx.HTTPError as e:
        logger.error(f"Erro ao enviar ações para o N8N: {e}")
