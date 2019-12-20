from rest_framework import viewsets, mixins
from rest_framework.response import *
from rest_framework.decorators import action
from rest_framework.status import *
from rest_framework.permissions import *
from .serializers import *
from .models import *
from .permissions import *
from django.db.models import Q

# Create your views here.


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.filter(is_deleted=False, last_version=True)
    versions_queryset = Story.objects.filter(is_deleted=False, is_draft=False)
    serializer_class = StorySerializer
    permission_classes = (StoryPermission,)
    update_pop_data = ['id', 'created_at', 'last_version']

    def get_queryset(self):
        request = self.request
        user = request.GET.get('user', None)
        if user == 'self':
            return self.queryset.filter(author=request.user)
        return self.queryset.filter(Q(author=request.user) | Q(is_draft=False))

    def perform_destroy(self, instance):
        self.versions_queryset.filter(seed=instance.seed).update(is_deleted=True)

    @action(detail=True, methods=['post'])
    def fork(self, request, pk=None):
        story = self.get_object()
        new_story = story.fork_story(request.user)
        serializer = StorySerializer(new_story)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def publish(self, request, pk=None):
        story = self.get_object()
        story.is_draft = False
        story.save()
        serializer = StorySerializer(story)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def new_version(self, request, pk=None):
        instance = self.get_object()
        if not instance.last_version:
            raise ValueError("need's to be a new version.")
        new_instance = instance.new_version_story()
        serializer = self.get_serializer(new_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        instance = self.get_object()
        query = self.versions_queryset.filter(seed=instance.seed)
        serializer = StorySerializer(query, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StoryHistoryViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = StoryHistory.objects.all()
    serializer_class = StoryHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-updated_at')

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
        serializer.save(user=self.request.user)