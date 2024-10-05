from celery import shared_task

from django.core.mail import send_mail

from yuhu.settings import EMAIL_HOST_USER


@shared_task
def send_task_created_email(event):
    subject = f'Task Created: {event['title']}'
    message = f'A new task has been created with ID: {event['task_id']}, title: {event['title']} and description: {event['description']}.'
    from_email = EMAIL_HOST_USER

    send_mail(subject, message, from_email, [event['email']])

@shared_task
def send_task_updated_email(event):
    subject = f'Task Updated: {event['title']}'
    message = f'A new task has been updated with ID: {event['task_id']}, title: {event['title']} and description: {event['description']}.'
    from_email = EMAIL_HOST_USER

    send_mail(subject, message, from_email, [event['email']])
