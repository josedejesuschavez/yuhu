import os
from django.contrib.auth import get_user_model

def run():
    username = 'jchavez'
    email = 'jchavez@example.com'  # Puedes cambiarlo a un email válido
    password = '123qweQWE'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')  # Cambia 'your_project_name' por el nombre de tu proyecto

    try:
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f'Superuser "{username}" created successfully.')
        else:
            print(f'Superuser "{username}" already exists.')
    except Exception as e:
        print(f'Error creating superuser: {e}')
