from pydantic import BaseModel


class ActionContent(BaseModel):
    type: str
    text: str


class Action(BaseModel):
    action: str
    channel: str
    conversation_id: str
    content: ActionContent


class ActionPayload(BaseModel):
    actions: list[Action]
