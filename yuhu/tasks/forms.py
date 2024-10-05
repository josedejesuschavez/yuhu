from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

class NewTaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

class AddDueDateForm(forms.Form):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'placeholder': 'Select date and time'
        })
    )

class UpdateTaskForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

