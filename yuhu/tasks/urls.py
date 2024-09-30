from django.urls import path
from .views import TaskView, TaskDetailView, LoginView, TaskAddDueDateView

urlpatterns = [
    path('tasks/', TaskView.as_view(), name='tasks_view'),
    path("tasks/<uuid:id>/", TaskDetailView.as_view(), name="tasks_detail_view"),
    path('tasks/add_due_date/<uuid:id>/', TaskAddDueDateView.as_view(), name='tasks_add_due_dateview'),
    path('login/', LoginView.as_view(), name='login'),
]
