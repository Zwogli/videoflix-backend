import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from app_videoflix.tasks import convert_480p
from .models import GlobalVideo, LocalVideo


@receiver(post_save, sender=GlobalVideo)
def video_global_post_save(sender, instance, created, **kwargs):
    if created:
        print('New global video created.')
        convert_480p(instance.file.path)
    else:
        print('Global video updated.')
        
        
@receiver(post_delete, sender=GlobalVideo)
def video_global_post_delete(sender, instance, **kwargs):
    """
    Deletes file from filessystem
    when corresponding `GlobalVideo` object is deleted
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
            print('Global-video is deleted.')


@receiver(post_save, sender=LocalVideo)
def video_local_post_save(sender, instance, created, **kwargs):
    if created:
        print('New local video created.')
        convert_480p(instance.file.path)
    else:
        print('Local video updated.')
        
        
@receiver(post_delete, sender=LocalVideo)
def video_global_post_delete(sender, instance, **kwargs):
    """
    Deletes file from filessystem
    when corresponding `LocalVideo` object is deleted
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
            print('Local-video is deleted.')