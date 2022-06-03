from django.urls import path, include
from rest_framework import routers
from .views import WorldViewSet


router = routers.SimpleRouter()
router.register('worlds', WorldViewSet)

urlpatterns = [
    path('', include(router.urls)),
]