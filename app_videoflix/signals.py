import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from django_rq import enqueue
from app_videoflix.tasks import convert, create_thumbnail, convert_480p, convert_720p
from .models import GlobalVideo, LocalVideo
import logging

logger = logging.getLogger('app_videoflix')
DEFAULT_QUEUE = 'default'
queue = django_rq.get_queue(DEFAULT_QUEUE, autocommit=True)


def get_file_name_without_extension(video_path):
    """
    Extracts the file name without the extension from the given video path.
    """
    return video_path.rsplit('.', 1)[0]


def queue_thumbnail_conversion(video_path, instance, is_global):
    """
    Enqueues the task to create a thumbnail for the video.
    """
    queue.enqueue(create_thumbnail, video_path, instance, is_global)


def queue_video_resolution_conversion(video_path, file_name):
    """
    Enqueues the tasks to convert the video into 480p and 720p resolutions.
    """
    queue.enqueue(convert_480p, video_path, file_name)
    queue.enqueue(convert_720p, video_path, file_name)


@receiver(post_save, sender=GlobalVideo)
def video_global_post_save(sender, instance, created, **kwargs):
    """
    Signal handler to process video tasks when a GlobalVideo instance is saved.
    
    Enqueues tasks for thumbnail creation and video conversion upon creation of a new global video.
    """
    if created:
        logger.info('New global video created: %s', instance.file.name)
        video_path = instance.file.path
        file_name = get_file_name_without_extension(video_path)
        queue_thumbnail_conversion(video_path, instance, is_global=True)
        queue_video_resolution_conversion(video_path, file_name)
    else:
        logger.info('Global video updated: %s', instance.file.name)
        
        
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
    """
    Signal handler to process video tasks when a LocalVideo instance is saved.
    
    Enqueues tasks for thumbnail creation and video conversion upon creation of a new local video.
    """
    if created:
        logger.info('New local video created: %s', instance.file.name)
        video_path = instance.file.path
        file_name = get_file_name_without_extension(video_path)
        print("File Name:", file_name)
        # create_thumbnail(video_path, instance, is_global=False)
        queue_thumbnail_conversion(video_path, instance, is_global=False)
        queue_video_resolution_conversion(video_path, file_name)
    else:
        logger.info('Local video updated: %s', instance.file.name)
        
        
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