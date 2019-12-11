from rest_framework import viewsets
from .serializers import *
from .models import *
from .permissions import *

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
