from pydantic import BaseModel


class EventContact(BaseModel):
    id: str
    phone: str
    push_name: str


class EventConversation(BaseModel):
    id: str
    is_group: bool


class EventMessage(BaseModel):
    id: str
    type: str
    text: str


class EventMetadata(BaseModel):
    connector: str
    instance: str
    source: str


class EventBody(BaseModel):
    event: str
    event_id: str
    trace_id: str
    channel: str
    timestamp: int
    contact: EventContact
    conversation: EventConversation
    message: EventMessage
    metadata: EventMetadata


class EventPayload(BaseModel):
    body: EventBody
