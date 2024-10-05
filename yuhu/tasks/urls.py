from django.urls import path

from tasks.views import LoginFormView, HomeView, NewTaskFormView, AddDueDateFormView, DeleteTaskFormView, UpdateTaskFormView

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('new-task/', NewTaskFormView.as_view(), name='new_task'),
    path('add-due-date/<int:id>/', AddDueDateFormView.as_view(), name='add_due_date'),
    path('delete_task/<int:id>/', DeleteTaskFormView.as_view(), name='delete_task'),
    path('update-task/<int:id>/', UpdateTaskFormView.as_view(), name='update_task'),
]
