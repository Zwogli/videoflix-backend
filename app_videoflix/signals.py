import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from django_rq import enqueue
from app_videoflix.tasks import convert, create_thumbnail, convert_480p, convert_720p
from .models import GlobalVideo, LocalVideo


def enqueue_video_conversion_tasks(video_path, file_name, is_global):
    """
    Helper function for adding video processing tasks to the queue.
    """
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(create_thumbnail, video_path, is_global=is_global)
    queue.enqueue(convert_480p, video_path, file_name)
    queue.enqueue(convert_720p, video_path, file_name)


def handle_video_deletion(video_path, thumbnail_path=None):
    """
    Helper function to delete the files of a video from the file system.
    """
    delete_file(video_path)
    delete_file(video_path.replace('.mp4', '_480p.mp4'))
    delete_file(video_path.replace('.mp4', '_720p.mp4'))
    if thumbnail_path:
        delete_file(thumbnail_path)


@receiver(post_save, sender=GlobalVideo)
def video_global_post_save(sender, instance, created, **kwargs):
    if created:
        print('New global video created.')
        video_path = instance.file.path
        file_name = video_path.split('.')
        enqueue_video_conversion_tasks(video_path, file_name, is_global=True)
    else:
        print('Global video updated.')


@receiver(post_delete, sender=GlobalVideo)
def video_global_post_delete(sender, instance, **kwargs):
    """
    Deletes the associated files when a GlobalVideo object is deleted.
    """
    video_path = instance.file.path
    thumbnail_path = instance.thumbnail.path if instance.thumbnail else None
    handle_video_deletion(video_path, thumbnail_path)
    print('Global video and associated files are deleted.')


@receiver(post_save, sender=LocalVideo)
def video_local_post_save(sender, instance, created, **kwargs):
    if created:
        print('New local video created.')
        video_path = instance.file.path
        file_name = video_path.split('.')
        enqueue_video_conversion_tasks(video_path, file_name, is_global=False)
    else:
        print('Local video updated.')


@receiver(post_delete, sender=LocalVideo)
def video_local_post_delete(sender, instance, **kwargs):
    """
    Deletes the associated files when a LocalVideo object is deleted.
    """
    video_path = instance.file.path
    thumbnail_path = instance.thumbnail.path if instance.thumbnail else None
    handle_video_deletion(video_path, thumbnail_path)
    print('Local video and associated files are deleted.')
            

def delete_file(file_path):
    if file_path and os.path.isfile(file_path):
        os.remove(file_path)
        print(f'File {file_path} deleted.')