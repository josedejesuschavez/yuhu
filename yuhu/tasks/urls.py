from django.urls import path
from .views import TaskView, TaskDetailView

urlpatterns = [
    path('tasks/', TaskView.as_view(), name='tasks_view'),
    path("tasks/<uuid:id>/", TaskDetailView.as_view(), name="tasks_detail_view"),
]
