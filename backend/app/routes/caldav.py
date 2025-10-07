import logging
from datetime import date, datetime

from fastapi import APIRouter, Request

from app.clients.caldav import CaldavClient
from app.core.config import settings
from app.exceptions import ServiceUnavailableError
from app.models.calendar import Calendar
from app.models.task import Task
from app.models.user import User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/caldav", tags=["caldav"])


@router.get("/calendars/{calendar_date}")
async def caldav_calendar(request: Request, calendar_date: date) -> list[Calendar | None]:
    # Redundant checks needed to satisfy the type system.
    if not settings.calendar_enabled or not settings.CALENDAR_URL:
        raise ServiceUnavailableError("Calendar")

    user: User = request.state.user
    access_token = user.access_token

    new_token = await exchange_token(access_token, audience=settings.CALENDAR_AUDIENCE)

    if not new_token:
        return []

    client = CaldavClient(base_url=settings.CALENDAR_URL, token=new_token)

    calendar_items: list[Calendar | None] = client.get_calendars(
        check_date=datetime.combine(calendar_date, datetime.min.time())
    )

    return calendar_items


@router.get("/tasks", response_model=list[Task])
async def caldav_tasks(request: Request) -> list[Task]:
    # Redundant checks needed to satisfy the type system.
    if not settings.task_enabled or not settings.TASK_URL:
        raise ServiceUnavailableError("Task")

    user: User = request.state.user
    access_token = user.access_token

    new_token = await exchange_token(access_token, audience=settings.TASK_AUDIENCE)

    if not new_token:
        return []

    client = CaldavClient(base_url=settings.TASK_URL, token=new_token)

    activities: list[Task] = client.get_tasks()

    return activities
