from django.urls import path

from .views import TokenAPIView

app_name = 'api'


urlpatterns = [
    path('tokens/', TokenAPIView.as_view()),
]
