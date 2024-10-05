from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from tasks.forms import LoginForm, NewTaskForm, AddDueDateForm, UpdateTaskForm
from tasks.services import get_all_tasks, insert_new_task, delete_task_by_id, update_task_by_id, add_due_date


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

        tasks = get_all_tasks()
        paginator = Paginator(tasks, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'home.html', {'page_obj': page_obj})

class NewTaskFormView(FormView):
    template_name = 'new_task.html'
    form_class = NewTaskForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        email = form.cleaned_data.get('email')
        description = form.cleaned_data.get('description')

        insert_new_task(title=title, email=email, description=description)

        return HttpResponseRedirect(self.success_url)


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

            add_due_date(id=id, due_date=due_date)
            return HttpResponseRedirect(self.success_url)
        except InvalidArgumentError as e:
            return HttpResponse(str(e))

class DeleteTaskFormView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        id = str(self.kwargs.get('id'))

        delete_task_by_id(id=id)
        return HttpResponseRedirect(reverse_lazy('home'))

class UpdateTaskFormView(FormView):
    template_name = 'update_task.html'
    form_class = UpdateTaskForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            id = self.kwargs.get('id')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            if title == '':
                title = None

            if description == '':
                description = None

            update_task_by_id(id=id, new_title=title, new_description=description)
            return HttpResponseRedirect(reverse_lazy('home'))
        except InvalidArgumentError as e:
            return HttpResponse(str(e))
