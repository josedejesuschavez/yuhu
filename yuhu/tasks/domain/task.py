import uuid
from typing import List

from shared.domain.entity import Entity
from shared.domain.invalid_argument_error import InvalidArgumentError
from tasks.domain.value_objects.task_description import TaskDescription
from tasks.domain.value_objects.task_due_date import TaskDueDate
from tasks.domain.value_objects.task_email import TaskEmail
from tasks.domain.value_objects.task_title import TaskTitle


class Task(Entity):

    def __init__(self,
                 id: str,
                 title: str,
                 email: str,
                 description: str,
                 due_date: int = None) -> None:
        super().__init__(id)
        self.title = TaskTitle(value=title)
        self.email = TaskEmail(value=email)
        self.description = TaskDescription(value=description)
        self.due_date = TaskDueDate(value=due_date)

    def update_due_date(self, new_due_date: int) -> None:
        self.due_date = TaskDueDate(value=new_due_date)

    @classmethod
    def create_task(cls, id: str, title: str, email: str, description: str, due_date: int = None) -> 'Task':
        return cls(
            id=id,
            title=title,
            email=email,
            description=description,
            due_date=due_date,
        )

    @classmethod
    def create_task_null(cls):
        return cls(
            id=str(uuid.UUID(int=0)),
            title='',
            email='empty@empty.com',
            description='',
            due_date=None
        )

    @staticmethod
    def verify_if_task_exists(task: "Task", tasks: List["Task"]) -> bool:
        id = task.id.value
        title = task.title.value.upper()
        filtered_by_id_tasks = list(
            filter(lambda task: task.id.value in id, tasks)
        )

        filtered_by_title_tasks = list(
            filter(lambda task: task.title.value.upper() in title, tasks)
        )
        if filtered_by_id_tasks:
            raise InvalidArgumentError(message=f"A task with id '{id}' already exists.", params=task.to_dict())

        if filtered_by_title_tasks:
            raise InvalidArgumentError(message=f"A task with title '{title}' already exists.", params=task.to_dict())

    def to_dict(self):
        return {
            "id": self.id.value,
            "title": self.title.value,
            "email": self.email.value,
            "description": self.description.value,
            "due_date": self.due_date.value,
            "due_date_format_date": self.due_date.from_timestamp()
        }