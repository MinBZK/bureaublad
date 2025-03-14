from datetime import datetime

from app.models import Calendar, Task
from caldav import DAVClient
from caldav.requests import HTTPBearerAuth


class CaldavClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token

        self.client = DAVClient(url=f"{base_url}/remote.php/dav", auth=HTTPBearerAuth(token))

    def get_calendars(self, check_date: datetime) -> list[Calendar | None]:
        principal = self.client.principal()
        calendars = principal.calendars()

        events_today: list[Calendar] = []

        for calendar in calendars:
            for event in calendar.events():
                event_instance = event.instance.vevent
                event_start = event_instance.dtstart.value
                event_end = event_instance.dtend.value

                if event_start <= check_date <= event_end:
                    events_today.append(Calendar(title=event_instance.summary.value, start=event_start, end=event_end))
        return events_today

    def get_tasks(self) -> list[Task]:
        principal = self.client.principal()
        calendars = principal.calendars()

        tasks_list: list[Task] = []

        for calendar in calendars:
            for task in calendar.todos():
                print(task.data)
                task_instance = task.instance.vtodo
                task_summary: str = task_instance.summary.value
                task_start: datetime = task_instance.dtstart.value
                task_due: datetime = task_instance.due.value

                tasks_list.append(Task(title=task_summary, start=task_start, end=task_due))

        return tasks_list
