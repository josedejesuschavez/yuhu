import uuid

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from shared.domain.invalid_argument_error import InvalidArgumentError
from tasks.application.add_due_date_to_a_task_use_case import AddDueDateToATaskUseCase
from tasks.application.delete_by_task_id_use_case import DeleteByTaskIdUseCase
from tasks.application.get_all_tasks_use_case import GetAllTasksUseCase
from tasks.application.insert_task_use_case import InsertTaskUseCase
from tasks.infrastructure.postgres_task_repository import PostgresRepository

task_repository = PostgresRepository()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class LoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)

class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):

        use_case = GetAllTasksUseCase(task_repository=task_repository)
        result = use_case.execute()
        paginator = Paginator(result, 1)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'home.html', {'page_obj': page_obj})

class NewTaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

class NewTaskFormView(FormView):
    template_name = 'new_task.html'
    form_class = NewTaskForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        id = str(uuid.uuid4())
        title = form.cleaned_data.get('title')
        email = form.cleaned_data.get('email')
        description = form.cleaned_data.get('description')

        use_case = InsertTaskUseCase(task_repository=task_repository)
        use_case.execute(id=id, title=title, email=email, description=description)

        return HttpResponseRedirect(self.success_url)

class AddDueDateForm(forms.Form):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'placeholder': 'Select date and time'
        })
    )

class AddDueDateFormView(FormView):
    template_name = 'add_due_date.html'
    form_class = AddDueDateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            id = self.kwargs.get('id')
            due_date = form.cleaned_data.get('due_date')

            id = str(id)
            due_date = int(due_date.timestamp())

            use_case = AddDueDateToATaskUseCase(task_repository=task_repository)
            use_case.execute(id=id, due_date=due_date)
            return HttpResponseRedirect(self.success_url)
        except InvalidArgumentError as e:
            return HttpResponse(str(e))

class DeleteTaskFormView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        id = str(self.kwargs.get('id'))

        use_case = DeleteByTaskIdUseCase(task_repository=task_repository)
        use_case.execute(id=id)
        return HttpResponseRedirect(reverse_lazy('home'))
