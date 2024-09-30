from django.urls import path

from tasks.views import LoginFormView, HomeView, NewTaskFormView, AddDueDateFormView, DeleteTaskFormView

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('new-task/', NewTaskFormView.as_view(), name='new_task'),
    path('add-due-date/<uuid:id>/', AddDueDateFormView.as_view(), name='add_due_date'),
    path('delete_task/<uuid:id>/', DeleteTaskFormView.as_view(), name='delete_task'),
]
