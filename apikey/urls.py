from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    Key as KeyViewSet
)

router = DefaultRouter()
router.register(r'', KeyViewSet)

urlpatterns = [
    path('', include(router.urls), name='API key actions'),
]