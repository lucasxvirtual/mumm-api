from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls import include
from django.urls import path


router = DefaultRouter()
router.register(r'story', StoryViewSet)
router.register(r'story-history', StoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
