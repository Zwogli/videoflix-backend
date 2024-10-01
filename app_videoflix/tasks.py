import subprocess
from .models import GlobalVideo, LocalVideo
import os


def convert(source):
    file_name = source.split('.')
    convert_480p(source, file_name)
    convert_720p(source, file_name)


def convert_480p(source, file_name):
    """
    Converts the source video into 480p resolution using ffmpeg.

    Args:
        source (str): The path to the source video file.
        file_name (list): The file name components split by '.' (used for naming the target file).

    The function uses subprocess to call ffmpeg and transcode the video to 480p.
    Raises an exception if the ffmpeg command fails.
    """
    target = file_name[0] + '_480p.mp4'
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        target
    ]
    subprocess.run(cmd, check=True) # check=True raises an exception if the command fails
    
    
def convert_720p(source, file_name):
    """
    Converts the source video into 720p resolution using ffmpeg.

    Args:
        source (str): The path to the source video file.
        file_name (list): The file name components split by '.' (used for naming the target file).

    The function uses subprocess to call ffmpeg and transcode the video to 720p.
    Raises an exception if the ffmpeg command fails.
    """
    target = file_name[0] + '_720p.mp4'
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd720',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        target
    ]
    subprocess.run(cmd, check=True) # check=True raises an exception if the command fails
    

def create_thumbnail(video_path, instance, is_global):
    thumbnail_path = set_thumbnail_path(video_path, is_global)
    check_thumbnail_path(thumbnail_path)    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-ss', '00:00:1.000',
        '-vframes', '1',
        thumbnail_path
    ]
    subprocess.run(cmd, check=True) # check=True raises an exception if the command fails
    relative_thumbnail_path = os.path.relpath(thumbnail_path, 'media/')
    instance.thumbnail = relative_thumbnail_path
    instance.thumbnail_created = True
    instance.save()
    

def set_thumbnail_path(video_path, is_global):
    if is_global:
        return video_path.replace('.mp4', '.jpg').replace('global_videos', 'global_thumbnails')
    else:
        return video_path.replace('.mp4', '.jpg').replace('local_videos', 'local_thumbnails')
    

def check_thumbnail_path(thumbnail_path):
    thumbnail_dir = os.path.dirname(thumbnail_path)
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir)