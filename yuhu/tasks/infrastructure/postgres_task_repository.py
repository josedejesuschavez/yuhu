from datetime import datetime
from typing import List

from tasks.domain.task import Task
from tasks.domain.task_repository import TaskRepository
from tasks.infrastructure.models import TaskModel


class PostgresRepository(TaskRepository):

    def get_task_by_id(self, id: str) -> Task:
        try:
            task_model = TaskModel.objects.get(uuid_id=id)

            task = Task.create_task(
                id=str(task_model.uuid_id),
                title=task_model.title,
                email=task_model.email,
                description=task_model.description,
            )
            return  task
        except TaskModel.DoesNotExist:
            return Task.create_task_null()

    def get_all_tasks(self) -> List[Task]:
        data = TaskModel.objects.all()

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
        TaskModel(
            uuid_id=task.id.value,
            title=task.title.value,
            email=task.email.value,
            description=task.description.value,
        ).save()

    def update_by_id(self, id: str, new_title: str = None, new_description: str = None, new_due_date: int = None) -> Task:
        try:
            task_model = TaskModel.objects.get(uuid_id=id)

            if new_title:
                task_model.title = new_title

            if new_description:
                task_model.description = new_description

            if new_due_date:
                task_model.due_date = datetime.fromtimestamp(new_due_date)

            task_model.save()

            task = Task.create_task(
                id=str(task_model.uuid_id),
                title=task_model.title,
                email=task_model.email,
                description=task_model.description,
                due_date=int(task_model.due_date.timestamp()) if task_model.due_date is not None else None,
            )
            return task
        except TaskModel.DoesNotExist:
            return Task.create_task_null()

    def delete_task_by_id(self, id: str):
        try:
            task_model = TaskModel.objects.get(uuid_id=id)

            task_model.delete()
            return Task.create_task(
                id=id,
                title=task_model.title,
                email=task_model.email,
                description=task_model.description,
                due_date=int(task_model.due_date.timestamp()) if task_model.due_date is not None else None,
            )
        except TaskModel.DoesNotExist:
            return Task.create_task_null()

