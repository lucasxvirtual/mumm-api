from rest_framework import viewsets, mixins
from rest_framework.status import *
from rest_framework.exceptions import *
from rest_framework.response import *
from rest_framework.permissions import *
from .serializers import *
from .models import *
from .permissions import *
from django.db.models import Q

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        user = self.request.user
        user_blocked = BlockUser.objects.filter(owner=user).values_list('user', flat=True)
        user_blocked_by = BlockUser.objects.filter(user=user).values_list('owner', flat=True)
        return self.queryset.exclude(Q(id__in=user_blocked) | Q(id__in=user_blocked_by))


class UserHistoryViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = UserHistory.objects.all()
    serializer_class = UserHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        user_blocked = BlockUser.objects.filter(owner=user).values_list('user', flat=True)
        user_blocked_by = BlockUser.objects.filter(user=user).values_list('owner', flat=True)
        return self.queryset.filter(owner=self.request.user)\
            .exclude(Q(id__in=user_blocked) | Q(id__in=user_blocked_by)).order_by('-updated_at')

    def create(self, request, *args, **kwargs):
        data = request.data
        already_in_history = self.get_queryset().filter(user=data['user'])
        if already_in_history:
            already_in_history[0].update_history()
            serializer = self.get_serializer(already_in_history[0])
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BlockUserViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = BlockUser.objects.all()
    serializer_class = BlockUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data['user'] == self.request.user:
            raise ValidationError("You can't block yourself")
        serializer.save(owner=self.request.user)
