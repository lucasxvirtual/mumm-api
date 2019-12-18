from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls import include, url
from django.urls import path
from rest_framework.authtoken import views


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'user-history', UserHistoryViewSet)

urlpatterns = [
    url(r'^auth/$', views.obtain_auth_token),
    path('', include(router.urls))
]
