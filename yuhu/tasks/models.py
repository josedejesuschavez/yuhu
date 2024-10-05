from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "email": self.email,
            "description": self.description,
            "due_date": self.due_date,
        }
