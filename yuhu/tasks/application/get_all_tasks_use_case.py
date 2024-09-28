from tasks.domain.task_repository import TaskRepository


class GetAllTasksUseCase:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self):
        tasks = self.task_repository.get_all_tasks()
        return [task.to_dict() for task in tasks]
