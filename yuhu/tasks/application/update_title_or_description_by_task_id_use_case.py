from shared.domain.invalid_argument_error import InvalidArgumentError
from shared.infrastructure.event_dispatcher import EventDispatcher
from tasks.domain.events.task_updated_event import TaskUpdatedEvent
from tasks.domain.task import Task
from tasks.domain.task_repository import TaskRepository
from tasks.infrastructure.task_updated_subscriber import TaskUpdatedSubscriber

class UpdateTitleOrDescriptionByTaskIdUseCase:

    def __init__(self, task_repository: TaskRepository, event_dispatcher = EventDispatcher()):
        self.task_repository = task_repository
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.subscribe(TaskUpdatedEvent, TaskUpdatedSubscriber())

    def execute(self, id: str, new_title: str = None, new_description: str = None):
        if new_title is None and new_description is None:
           raise InvalidArgumentError(message='No parameters provided for update.', params={})

        task_updated = self.task_repository.update_by_id(
            id=id,
            new_title=new_title,
            new_description=new_description)

        if task_updated.equals(Task.create_task_null()):
            raise InvalidArgumentError(message=f"Task '{id}' not found.", params={})

        event = TaskUpdatedEvent(task_id=id, title=new_title, email=task_updated.email.value, description=new_description)
        self.event_dispatcher.dispatch(event)
