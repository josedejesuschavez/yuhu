from tasks.domain.task import Task
from tasks.domain.task_repository import TaskRepository


class InsertTaskUseCase:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, id: str, title: str, email: str, description: str):
        new_task = Task.create_task(id=id, title=title, email=email, description=description)
        tasks = self.task_repository.get_all_tasks()
        Task.verify_if_task_exists(task=new_task, tasks=tasks)
        self.task_repository.insert_task(new_task)
        return new_task.to_dict()