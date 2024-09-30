from tasks.domain.task_repository import TaskRepository


class AddDueDateToATaskUseCase:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, id: str, due_date: int):
        task = self.task_repository.get_task_by_id(id=id)

        task.update_due_date(new_due_date=due_date)
        self.task_repository.update_by_id(id=id, new_due_date=due_date)
        return task.to_dict()
