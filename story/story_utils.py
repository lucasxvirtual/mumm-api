from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import *
import binascii
import os


@receiver(pre_save, sender=Story)
def set_story_seed(sender, instance=None, **kwargs):
    if instance.seed != '':
        return
    instance.seed = generate_seed()


def generate_seed():
    seed = binascii.hexlify(os.urandom(20)).decode()
    while Story.objects.filter(seed=seed):
        seed = binascii.hexlify(os.urandom(20)).decode()
    return seed
