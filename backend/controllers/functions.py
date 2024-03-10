from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime, timedelta


# class CalendyEvent(BaseModel):
#     """Cancel a scheduled event."""

#     get_scheduled_events: bool = Field(
#         False,
#         description="Return true if asked for cancel a event otherwise return false",
#     )

#     meeting_name: str = Field(..., description="Get the Name of the event to cancel")

#     time: str = Field(
#         ..., description="Get the Time of the event to cancel in %H:%M:%S format"
#     )

#     day: str = Field(
#         ...,
#         description="Get the Day of the event to cancel. If it contains Today, Tomorrow or Yesterday, return it as it is otherwise return in %Y-%m-%d format",
#     )


class CancelEvent(BaseModel):
    """Cancel an event. Extract the meeting name, start date and end date of the event to cancel. It could be possible that only one of them is present"""

    meeting_name: str = Field(..., description="Get the Name of the event to cancel")

    time: str = Field(
        ..., description="Get the Time of the event to cancel in %H:%M:%S format"
    )

    day: str = Field(
        ...,
        description="Get the Day of the event to cancel. If it contains Today, Tomorrow or Yesterday, return it as it is otherwise return in %Y-%m-%d format",
    )


class GetScheduledEvents(BaseModel):
    """Return true if asked for extracting list of all events."""

    get_scheduled_events: bool = Field(
        ...,
        description="Return true if asked for extracting list of all events",
    )


class CreateEvent(BaseModel):
    """Create a new event. Extract the name, duration, start date and end date of the event to create."""

    name: str = Field("My Meeting", description="Get the Name of the event to create")

    duration: str = Field(
        ...,
        description="Get the Duration of the event to create in %M format. Set default as 30 mins if not present.",
    )

    start_date: str = Field(
        ...,
        description=f"Get the Start Time of the event to create in %Y-%m-%d format. If start date is not present then, use the current date {datetime.now().date()}",
    )

    end_date: str = Field(
        ...,
        description=f"Get the End Time of the event to create in %Y-%m-%d format. If end date is not present then, use {datetime.now().date() +  timedelta(days=7)}.",
    )


class GeneralChat(BaseModel):
    """Return summary of the input in a markdown format."""

    description: str = Field(
        ...,
        description="Return summary of the input. Make it in markdown format. If needed, show as bullet points, if there are link then display as link with color blue. Put output like a general chat bot response.",
    )
