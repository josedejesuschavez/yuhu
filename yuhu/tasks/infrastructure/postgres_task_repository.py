from typing import List

from tasks.domain.task import Task
from tasks.domain.task_repository import TaskRepository
from tasks.infrastructure.models import TaskModel


class PostgresRepository(TaskRepository):

    def get_task_by_id(self, id: str) -> Task:
        try:
            task_model = TaskModel.objects.get(id=id)

            task = Task.create_task(
                id=str(task_model.id),
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
                id=str(task.id),
                title=task.title,
                email=task.email,
                description=task.description,
            )
            for task in data
        ]

    def insert_task(self, task: Task):
        TaskModel(
            id=task.id.value,
            title=task.title.value,
            email=task.email.value,
            description=task.description.value,
        ).save()

    def update_title_or_description_by_id(self, id: str, new_title: str, new_description: str) -> Task:
        try:
            task_model = TaskModel.objects.get(id=id)

            if new_title:
                task_model.title = new_title

            if new_description:
                task_model.description = new_description

            task_model.save()

            task = Task.create_task(
                id=str(task_model.id),
                title=task_model.title,
                email=task_model.email,
                description=task_model.description,
            )
            return task
        except TaskModel.DoesNotExist:
            return Task.create_task_null()

    def delete_task_by_id(self, id: str):
        try:
            task_model = TaskModel.objects.get(id=id)

            task_model.delete()
            return Task.create_task(
                id=id,
                title=task_model.title,
                email=task_model.email,
                description=task_model.description,
            )
        except TaskModel.DoesNotExist:
            return Task.create_task_null()

