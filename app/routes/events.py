from fastapi import APIRouter, BackgroundTasks, Depends
from app.core.security import verify_api_key
from app.schemas.events import EventPayload
from app.services.event_handler import process_event

router = APIRouter()


@router.post("/events")
async def events(
    payload: list[EventPayload],
    background_tasks: BackgroundTasks,
    auth=Depends(verify_api_key),
):
    for event in payload:
        if event.body.event == "message.received":
            background_tasks.add_task(process_event, event.body)

    return {"status": "accepted"}
