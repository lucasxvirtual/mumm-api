from rest_framework import viewsets
from rest_framework.response import *
from rest_framework.decorators import action
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
