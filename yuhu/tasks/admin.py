from django.contrib import admin

from tasks.infrastructure.models import TaskModel

admin.site.register(TaskModel)
