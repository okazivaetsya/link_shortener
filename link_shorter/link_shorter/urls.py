from django.contrib import admin
from django.urls import path, include
from api import services


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('<str:short_url>', services.redirection),
]
