from django.db import models
from mumm.settings import *
from django.utils import timezone

# Create your models here.


class Story(models.Model):
    thumbnail = models.ImageField(null=True)
    title = models.CharField(max_length=100)
    text = models.TextField(null=True)
    is_draft = models.BooleanField(default=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    seed = models.CharField(max_length=250, blank=True, default='')
    is_deleted = models.BooleanField(default=False)
    last_version = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def fork_story(self, user):
        from .story_utils import generate_seed
        old_id = self.id
        self.id = None
        self.author = user
        self.parent = Story.objects.get(pk=old_id)
        self.created_at = timezone.now()
        self.is_draft = True
        self.seed = generate_seed()
        self.save()
        return self

    def new_version_story(self):
        old_id = self.id
        self.id = None
        self.created_at = timezone.now()
        self.save()
        Story.objects.filter(pk=old_id).update(last_version=False)
        return self
