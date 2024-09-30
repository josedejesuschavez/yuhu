import uuid
from pydoc import describe
from unittest.mock import Mock

import pytest
from typing import List

from django.template.defaultfilters import title
from model_bakery import baker

from shared.domain.invalid_argument_error import InvalidArgumentError
from tasks.application.delete_by_task_id_use_case import DeleteByTaskIdUseCase
from tasks.application.get_all_tasks_use_case import GetAllTasksUseCase
from tasks.application.insert_task_use_case import InsertTaskUseCase
from tasks.domain.task import Task
from tasks.domain.task_repository import TaskRepository
from tasks.infrastructure.models import TaskModel


class FakeTaskRepository(TaskRepository):

    def __init__(self):
        self.data = []

    def get_task_by_id(self, id: str) -> Task:
        pass

    def get_all_tasks(self) -> List[Task]:
        data = self.data

        return [
            Task.create_task(
                id=str(task.uuid_id),
                title=task.title,
                email=task.email,
                description=task.description,
                due_date=int(task.due_date.timestamp()) if task.due_date is not None else None,
            )
            for task in data
        ]

    def insert_task(self, task: Task):
        task = baker.make(
            TaskModel,
            uuid_id=task.id.value,
            title=task.title.value,
            email=task.email.value,
            description=task.description.value,
        )
        self.data.append(task)

    def update_by_id(self, id: str, new_title: str = None, new_description: str = None, new_due_date: int = None):
        pass

    def delete_task_by_id(self, id: str):
        for i in self.data:
            if i.uuid_id == id:
                self.data.remove(i)
                return Task.create_task(
                    id=id,
                    title=i.title,
                    email=i.email,
                    description=i.description,
                    due_date=int(i.due_date.timestamp()) if i.due_date is not None else None,
                )

        return Task.create_task_null()

class FakeEventDispatcher:

    def subscribe(self, event_type, subscriber):
        return None

    def dispatch(self, event):
        return None


def test_get_all_tasks_use_case_happy_path():
    use_case = GetAllTasksUseCase(task_repository=FakeTaskRepository())
    result = use_case.execute()
    assert len(result) == 0

@pytest.mark.django_db
def test_insert_task_use_case_happy_path():
    id = str(uuid.uuid4())
    title = 'fakeTest'
    email = 'fake@email.com'
    description = 'fakeDescription'

    use_case = InsertTaskUseCase(task_repository=FakeTaskRepository(), event_dispatcher=FakeEventDispatcher())
    result = use_case.execute(
        id=id,
        title=title,
        email=email,
        description=description,
    )
    assert result == {
        'id': id,
        'title': title,
        'email': email,
        'description': description,
        'due_date': None, 'due_date_format_date': None
    }


@pytest.mark.django_db
def test_delete_by_task_id_use_case_happy_path():
    id = str(uuid.uuid4())
    title = 'fakeTest'
    email = 'fake@email.com'
    description = 'fakeDescription'

    task_repository = FakeTaskRepository()
    use_case = InsertTaskUseCase(task_repository=task_repository, event_dispatcher=FakeEventDispatcher())
    use_case.execute(
        id=id,
        title=title,
        email=email,
        description=description,
    )

    use_case = DeleteByTaskIdUseCase(task_repository=task_repository)
    result = use_case.execute(id=id)

    assert result is None

@pytest.mark.django_db
def test_delete_by_task_id_use_case_when_task_not_exist():
    id = str(uuid.uuid4())
    title = 'fakeTest'
    email = 'fake@email.com'
    description = 'fakeDescription'

    task_repository = FakeTaskRepository()
    use_case = InsertTaskUseCase(task_repository=task_repository, event_dispatcher=FakeEventDispatcher())
    use_case.execute(
        id=id,
        title=title,
        email=email,
        description=description,
    )

    use_case = DeleteByTaskIdUseCase(task_repository=task_repository)

    id_delete = str(uuid.uuid4())
    with pytest.raises(InvalidArgumentError) as exc_info:
        use_case.execute(id=id_delete)

    assert str(exc_info.value) == f"Task '{id_delete}' not found. {{}}"
