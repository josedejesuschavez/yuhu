import uuid

from django.db import models


class TaskModel(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.title
