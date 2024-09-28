from tasks.domain.events.task_updated_event import TaskUpdatedEvent
from tasks.tasks import send_task_updated_email

class TaskUpdatedSubscriber:
    def handle(self, event: TaskUpdatedEvent):
        send_task_updated_email.delay(event)