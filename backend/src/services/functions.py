from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime, timedelta


class CancelEvent(BaseModel):
    """Cancel the given event. This is done by extracting the meeting name, start date and end date from the event description."""

    meeting_name: str = Field(..., description="Get the Name of the event to cancel. If not present, set default as 'My Meeting'")
    time: str = Field(..., description="Get the Time of the event to cancel in %H:%M:%S format")
    day: str = Field(..., description="Get the Day of the event to cancel. If it contains Today, Tomorrow or Yesterday, return it as it is otherwise return in %Y-%m-%d format")
    reason: str = Field(..., description="Get the Reason for the event to cancel. If not present, set default as 'Not well'.")
    all_events: bool = Field(..., description="Return true if asked for cancelling all events. Default is False.")


class GetScheduledEvents(BaseModel):
    """Return true if asked for extracting list of all events."""

    get_scheduled_events: bool = Field(..., description="Return true if asked for extracting list of all events" )


class CreateEvent(BaseModel):
    """Create a new event. Extract the name, duration, start date and end date of the event to create."""

    name: str = Field(..., description="Get the Name of the event to create. Set default as 'My Meeting'")
    duration: str = Field(..., description="Get the Duration of the event to create in %M format. Set default as 30 mins if not present.")
    start_date: str = Field(..., description=f"Get the Start Time of the event to create in %Y-%m-%d format. If start date is not present then, use the current date {datetime.now().date()}")
    end_date: str = Field(..., description=f"Get the End Time of the event to create in %Y-%m-%d format. If end date is not present then, use {datetime.now().date() +  timedelta(days=7)}." )


class GeneralChat(BaseModel):
    """Return formatted output in a markdown format."""

    description: str = Field(
        ...,
        description="""Reformat the input in a presentable format. 
        Make it in markdown format. Put output like a general chat bot response.
        
        If needed, show as bullet points, if there are link then display as 
        link with color blue. If not present, set default as 'No event scheduled'.

        If its about cancelling an event, then dont forget to add the reason for the cancellation.""",
    )
