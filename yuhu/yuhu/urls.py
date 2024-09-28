from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("api/", include("tasks.urls")),
]
