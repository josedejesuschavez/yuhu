from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TaskAPIView(APIView):

    # Manejar el verbo GET
    def get(self, request, *args, **kwargs):
        data = {"message": "GET request - Obtener datos"}
        return Response(data, status=status.HTTP_200_OK)

    # Manejar el verbo POST
    def post(self, request, *args, **kwargs):
        received_data = request.data  # Obtenemos los datos enviados en el cuerpo de la solicitud
        data = {"message": "POST request - Crear datos", "received_data": received_data}
        return Response(data, status=status.HTTP_201_CREATED)

    # Manejar el verbo PUT
    def put(self, request, *args, **kwargs):
        received_data = request.data  # Obtenemos los datos enviados en el cuerpo de la solicitud
        data = {"message": "PUT request - Actualizar datos", "updated_data": received_data}
        return Response(data, status=status.HTTP_200_OK)

    # Manejar el verbo DELETE
    def delete(self, request, *args, **kwargs):
        data = {"message": "DELETE request - Eliminar datos"}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
