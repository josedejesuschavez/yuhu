from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=100)
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