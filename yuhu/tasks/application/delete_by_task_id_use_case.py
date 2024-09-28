from shared.domain.invalid_argument_error import InvalidArgumentError
from tasks.domain.task import Task
from tasks.domain.task_repository import TaskRepository


class DeleteByTaskIdUseCase:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, id: str):
        task_deleted = self.task_repository.delete_task_by_id(id=id)
        if task_deleted.equals(Task.create_task_null()):
            raise InvalidArgumentError(message=f"Task '{id}' not found.", params={})
