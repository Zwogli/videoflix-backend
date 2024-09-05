import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from django_rq import enqueue

from app_videoflix.tasks import convert, create_thumpnail
from .models import GlobalVideo, LocalVideo


@receiver(post_save, sender=GlobalVideo)
def video_global_post_save(sender, instance, created, **kwargs):
    if created:
        print('New global video created.')
        video_path = instance.file.path
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert, video_path)
        
        # convert(video_path)
        create_thumpnail(video_path, instance, is_global=True)
    else:
        print('Global video updated.')
        
        
@receiver(post_delete, sender=GlobalVideo)
def video_global_post_delete(sender, instance, **kwargs):
    """
    Deletes file from filessystem
    when corresponding `GlobalVideo` object is deleted
    """
    video_path = instance.file.path
    video_path_480p = video_path.replace('.mp4', '_480p.mp4')
    video_path_720p = video_path.replace('.mp4', '_720p.mp4')
    thumbnail_path = instance.thumbnail.path if instance.thumbnail else None
    
    delete_file(video_path)
    delete_file(video_path_480p)
    delete_file(video_path_720p)
    delete_file(thumbnail_path)
    
    print('Global-video and associated files are deleted.')


@receiver(post_save, sender=LocalVideo)
def video_local_post_save(sender, instance, created, **kwargs):
    if created:
        print('New local video created.')
        video_path = instance.file.path
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert, video_path)
        # convert(video_path)
        create_thumpnail(video_path, instance, is_global=False)
    else:
        print('Local video updated.')
        
        
@receiver(post_delete, sender=LocalVideo)
def video_local_post_delete(sender, instance, **kwargs):
    """
    Deletes file from filessystem
    when corresponding `LocalVideo` object is deleted
    """
    video_path = instance.file.path
    video_path_480p = video_path.replace('.mp4', '_480p.mp4')
    video_path_720p = video_path.replace('.mp4', '_720p.mp4')
    thumbnail_path = instance.thumbnail.path if instance.thumbnail else None
    
    delete_file(video_path)
    delete_file(video_path_480p)
    delete_file(video_path_720p)
    delete_file(thumbnail_path)
    
    print('Local-video and associated files are deleted.')
            

def delete_file(file_path):
    if file_path and os.path.isfile(file_path):
        os.remove(file_path)
        print(f'File {file_path} deleted.')