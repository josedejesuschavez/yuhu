from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.domain.invalid_argument_error import InvalidArgumentError
from tasks.application.add_due_date_to_a_task_use_case import AddDueDateToATaskUseCase
from tasks.application.delete_by_task_id_use_case import DeleteByTaskIdUseCase
from tasks.application.get_all_tasks_use_case import GetAllTasksUseCase
from tasks.application.insert_task_use_case import InsertTaskUseCase
from tasks.application.update_title_or_description_by_task_id_use_case import UpdateTitleOrDescriptionByTaskIdUseCase
from tasks.infrastructure.postgres_task_repository import PostgresRepository


task_repository = PostgresRepository()

class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    title = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=True)
    description = serializers.CharField(required=True)

class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False)

class TaskAddDueDateSerializer(serializers.Serializer):
    due_date = serializers.IntegerField(required=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


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


        use_case = GetAllTasksUseCase(task_repository=task_repository)
        result = use_case.execute()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(result, request)
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

                id = str(validated_data['id'])
                title = validated_data['title']
                email = validated_data['email']
                description = validated_data['description']

                use_case = InsertTaskUseCase(task_repository=task_repository)
                result = use_case.execute(id=id, title=title, email=email, description=description)
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

                use_case = UpdateTitleOrDescriptionByTaskIdUseCase(task_repository=task_repository)
                use_case.execute(id=str(id), new_title=title, new_description=description)
                return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)
        except InvalidArgumentError as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            use_case = DeleteByTaskIdUseCase(task_repository=task_repository)
            use_case.execute(id=str(id))
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
    def post(self, request, id):
        try:
            serializer = TaskAddDueDateSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                due_date = int(validated_data['due_date'])
                use_case = AddDueDateToATaskUseCase(task_repository=task_repository)
                result = use_case.execute(id=str(id), due_date=due_date)
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
