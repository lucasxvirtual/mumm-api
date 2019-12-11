from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls import include, url
from django.urls import path


router = DefaultRouter()
router.register(r'^', UserViewSet)

urlpatterns = [

    path('', include(router.urls))
]
