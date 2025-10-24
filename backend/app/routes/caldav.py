import logging
from datetime import date, datetime

from fastapi import APIRouter, Request

from app.clients.caldav import CaldavClient
from app.core.config import settings
from app.exceptions import ServiceUnavailableError
from app.models.calendar import Calendar
from app.models.task import Task
from app.token_exchange import get_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/caldav", tags=["caldav"])


async def get_caldav_client(request):
    if not settings.task_enabled or not settings.TASK_URL:
        raise ServiceUnavailableError("Task")

    # Get auth from session (already refreshed by get_current_user dependency)
    new_token = await get_token(request, settings.TASK_AUDIENCE)

    client = CaldavClient(base_url=settings.TASK_URL, token=new_token)
    return client


@router.get("/calendars/{calendar_date}")
async def caldav_calendar(
    calendar_date: date,
    request: Request,
) -> list[Calendar | None]:
    """Get calendar events for a specific date.

    Note: Auth is validated by get_current_user() at router level.
    """
    client = await get_caldav_client(request)

    calendar_items: list[Calendar | None] = client.get_calendars(
        check_date=datetime.combine(calendar_date, datetime.min.time())
    )

    return calendar_items


@router.get("/tasks", response_model=list[Task])
async def caldav_tasks(request: Request) -> list[Task]:
    """Get tasks from CalDAV service.

    Note: Auth is validated by get_current_user() at router level.
    """
    client = await get_caldav_client(request)

    activities: list[Task] = client.get_tasks()

    return activities
