from tasks.domain.events.task_created_event import TaskCreatedEvent
from tasks.tasks import send_task_created_email

class TaskCreatedSubscriber:
    def handle(self, event: TaskCreatedEvent):
        send_task_created_email.delay(event)
