from .models import videos_global, videos_local
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=videos_global)
def video_global_post_save(sender, instance, created, **kwargs):
    print('Global Video wurde gespeichert.')
    if created:
        print('New global video created.')
    else:
        print('Global video updated.')


@receiver(post_save, sender=videos_local)
def video_local_post_save(sender, instance, created, **kwargs):
    print('Local Video wurde gespeichert.')
    if created:
        print('New local video created.')
    else:
        print('Local video updated.')