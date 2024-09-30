from datetime import datetime

import pytest

from shared.domain.invalid_argument_error import InvalidArgumentError
from tasks.domain.value_objects.task_due_date import TaskDueDate
from tasks.domain.value_objects.task_email import TaskEmail
from tasks.domain.value_objects.task_title import TaskTitle


def test_task_date_valid():
    current_due_date = int(datetime.now().timestamp())
    value_object = TaskDueDate(value=current_due_date)
    assert value_object.value == current_due_date

def test_task_date_when_due_date_is_in_the_past():
    current_due_date = 1

    with pytest.raises(InvalidArgumentError) as exc_info:
        TaskDueDate(value=current_due_date)

    assert str(exc_info.value) == f"The due date '{current_due_date}' cannot be in the past. {{}}"

def test_task_email_valid():
    email='email@email.com'
    value_object = TaskEmail(value=email)
    assert value_object.value == email

def test_task_email_invalid():
    email = 'email@'

    with pytest.raises(InvalidArgumentError) as exc_info:
        TaskEmail(value=email)

    assert str(exc_info.value) == f"'{email}' is not a valid email address. {{}}"

def test_task_title_valid():
    title = 'title'
    value_object = TaskTitle(value=title)
    assert value_object.value == title

def test_task_title_length_not_valid():
    title = '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'

    with pytest.raises(InvalidArgumentError) as exc_info:
        TaskTitle(value=title)

    assert str(exc_info.value) == f"The title cannot exceed 100 characters. {{'value': '{title}'}}"
