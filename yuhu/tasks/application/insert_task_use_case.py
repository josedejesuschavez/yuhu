from shared.infrastructure.event_dispatcher import EventDispatcher
from tasks.domain.events.task_created_event import TaskCreatedEvent
from tasks.domain.task import Task
from tasks.domain.task_repository import TaskRepository
from tasks.infrastructure.task_created_subscriber import TaskCreatedSubscriber


class InsertTaskUseCase:

    def __init__(self, task_repository: TaskRepository, event_dispatcher: EventDispatcher = EventDispatcher()):
        self.task_repository = task_repository
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.subscribe(TaskCreatedEvent, TaskCreatedSubscriber())

    def execute(self, id: str, title: str, email: str, description: str):
        new_task = Task.create_task(id=id, title=title, email=email, description=description)
        tasks = self.task_repository.get_all_tasks()
        Task.verify_if_task_exists(task=new_task, tasks=tasks)
        self.task_repository.insert_task(new_task)
        event = TaskCreatedEvent(task_id=id, title=title, email=email, description=description)
        self.event_dispatcher.dispatch(event)
        return new_task.to_dict()