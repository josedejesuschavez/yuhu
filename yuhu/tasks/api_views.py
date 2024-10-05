from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.exceptions import InvalidArgumentError
from tasks.serializers import TaskSerializer, TaskUpdateSerializer, TaskAddDueDateSerializer, LoginSerializer
from tasks.services import get_all_tasks, insert_new_task, delete_task_by_id, update_task_by_id, add_due_date


class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@extend_schema(
    parameters=[
        OpenApiParameter('page', int, description="Número de la página", required=False),
        OpenApiParameter('page_size', int, description="Número de tareas por página", required=False),
    ]
)
class TaskView(ListCreateAPIView):
    pagination_class = TaskPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tasks = get_all_tasks()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(tasks, request)
        return paginator.get_paginated_response(result_page)

    @extend_schema(
        request=TaskSerializer,
        responses={201: TaskSerializer, 400: 'Invalid data'},
        operation_id='createTask',
        summary='Create a new task',
        description='Creates a new task with a id, title, email, and description.',
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = TaskSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                title = validated_data['title']
                email = validated_data['email']
                description = validated_data['description']

                result = insert_new_task(title=title, email=email, description=description)
                return Response(result, status=status.HTTP_201_CREATED)
        except InvalidArgumentError as e:
            return Response(str(e), status=status.HTTP_409_CONFLICT)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TaskUpdateSerializer,
        responses={201: TaskUpdateSerializer, 400: 'Invalid data'},
        operation_id='updateTask',
        summary='Update a task',
        description='Update task.',
    )
    def put(self, request, id):
        try:
            serializer = TaskUpdateSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                title = validated_data.get('title')
                description = validated_data.get('description')

                update_task_by_id(id=id, new_title=title, new_description=description)
                return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)
        except InvalidArgumentError as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            delete_task_by_id(id=id)
            return Response({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)
        except InvalidArgumentError as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

class TaskAddDueDateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TaskAddDueDateSerializer,
        responses={201: TaskAddDueDateSerializer, 400: 'Invalid data'},
        operation_id='addDueDateTask',
        summary='Add due date to Task',
        description='Add due Date.',
    )
    def put(self, request, id):
        try:
            serializer = TaskAddDueDateSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                due_date = int(validated_data['due_date'])

                result = add_due_date(id=id, due_date=due_date)
                return Response(result, status=status.HTTP_201_CREATED)
        except InvalidArgumentError as e:
            return Response(str(e), status=status.HTTP_409_CONFLICT)

class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={201: LoginSerializer, 400: 'Invalid data'},
        operation_id='login',
        summary='Login',
        description='Login.',
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
