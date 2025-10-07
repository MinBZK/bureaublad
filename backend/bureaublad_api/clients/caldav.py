# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportAssignmentType=false
from datetime import date, datetime

from bureaublad_api.models.calendar import Calendar
from bureaublad_api.models.task import Task
from caldav import DAVClient
from caldav.requests import HTTPBearerAuth


class CaldavClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token

        self.client = DAVClient(url=f"{base_url}/remote.php/dav", auth=HTTPBearerAuth(token))

    def get_calendars(self, check_date: date) -> list[Calendar | None]:
        principal = self.client.principal()
        calendars = principal.calendars()

        events_today: list[Calendar | None] = []

        for calendar in calendars:
            check_date_start = datetime.combine(check_date, datetime.min.time())
            check_date_end = datetime.combine(check_date, datetime.max.time())
            events = calendar.search(start=check_date_start, end=check_date_end, event=True, expand=True)
            for event in events:
                event_instance = event.instance.vevent
                events_today.append(
                    Calendar(
                        title=event_instance.summary.value,
                        start=event_instance.dtstart.value,
                        end=event_instance.dtend.value,
                    )
                )

        return events_today

    def get_tasks(self) -> list[Task]:
        principal = self.client.principal()
        calendars = principal.calendars()

        tasks_list: list[Task] = []

        for calendar in calendars:
            for task in calendar.todos():
                task_instance = task.instance.vtodo
                task_summary: str = task_instance.summary.value
                task_start: datetime = task_instance.dtstart.value if hasattr(task_instance, "dtstart") else None
                task_due: datetime = task_instance.due.value if hasattr(task_instance, "due") else None
                tasks_list.append(Task(title=task_summary, start=task_start, end=task_due))

        return tasks_list
