from django.urls import path
from .views import ListWorldView


urlpatterns = [
    path('world/', ListWorldView.as_view(), name="world-all")
]