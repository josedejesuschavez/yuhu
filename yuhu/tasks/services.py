from datetime import datetime

from tasks.events import TaskUpdatedEvent, TaskCreatedEvent
from tasks.exceptions import InvalidArgumentError
from tasks.models import Task
from tasks.tasks import send_task_created_email, send_task_updated_email


def get_all_tasks():
    tasks = Task.objects.all()
    return [task.to_dict() for task in tasks]

def insert_new_task(title: str, email: str, description: str):
    tasks_with_same_title = Task.objects.filter(title__iexact=title.upper())

    if tasks_with_same_title:
        raise InvalidArgumentError(message=f"A task with title '{title}' already exists.", params={})

    task = Task(title=title, email=email, description=description)
    task.save()

    event = TaskCreatedEvent(task_id=id, title=title, email=email, description=description)

    send_task_created_email.delay(event)
    return task.to_dict()

def delete_task_by_id(id: int):
    try:
        task = Task.objects.get(id=id)

        task.delete()
    except Task.DoesNotExist:
        raise InvalidArgumentError(message=f"A task with id '{id}' not exists.", params={})

def update_task_by_id(id: int, new_title: str, new_description: str):
    if new_title is None and new_description is None:
        raise InvalidArgumentError(message='No parameters provided for update.', params={})

    try:
        task = Task.objects.get(id=id)

        if new_title is not None:
            task.title = new_title

        if new_description is not None:
            task.description = new_description

        task.save()

        event = TaskUpdatedEvent(task_id=id, title=new_title, email=task.email, description=new_description)
        send_task_updated_email.delay(event)
    except Task.DoesNotExist:
        raise InvalidArgumentError(message=f"A task with id '{id}' not exists.", params={})

def add_due_date(id: int, due_date: int):
    try:
        task = Task.objects.get(id=id)

        task.due_date = datetime.fromtimestamp(due_date)
        task.save()
        return task.to_dict()
    except Task.DoesNotExist:
        raise InvalidArgumentError(message=f"A task with id '{id}' not exists.", params={})
