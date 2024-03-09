from langchain_core.pydantic_v1 import BaseModel, Field

class CancelEvent(BaseModel):
    """Cancel a scheduled event."""
    
    get_scheduled_events: bool = Field(False, description="Return true if asked for cancel a event otherwise return false")
    event_id: str = Field(..., description="Get the ID of the event to cancel")
    time: str = Field(..., description="Get the Time of the event to cancel in 24 hour format")
    day: str = Field(..., description="Get the Day of the event to cancel")

