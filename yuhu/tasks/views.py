from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.domain.invalid_argument_error import InvalidArgumentError
from tasks.application.delete_by_task_id_use_case import DeleteByTaskIdUseCase
from tasks.application.get_all_tasks_use_case import GetAllTasksUseCase
from tasks.application.insert_task_use_case import InsertTaskUseCase
from tasks.application.update_title_or_description_by_task_id_use_case import UpdateTitleOrDescriptionByTaskIdUseCase
from tasks.infrastructure.postgres_task_repository import PostgresRepository

task_repository = PostgresRepository()


class TaskSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    description = serializers.CharField()

class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False)


class TaskView(APIView):

    def get(self, request, *args, **kwargs):
        use_case = GetAllTasksUseCase(task_repository=task_repository)
        result = use_case.execute()
        return Response(result, status=status.HTTP_200_OK)

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
