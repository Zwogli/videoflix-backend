import subprocess
from .models import GlobalVideo, LocalVideo
import os
import logging


logger = logging.getLogger('app_videoflix')


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
    run_ffmpeg_command(cmd)
    
    
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
    run_ffmpeg_command(cmd)
    

def create_thumbnail(video_path, instance, is_global):
    """
    Creates a thumbnail for the video and saves the path in the instance.

    Args:
        video_path (str): The path to the video file.
        instance (Model): The video model instance (GlobalVideo or LocalVideo).
        is_global (bool): Indicates if the video is global or local.
    """
    thumbnail_path = set_thumbnail_path(video_path, is_global)
    check_thumbnail_path(thumbnail_path)    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-ss', '00:00:1.000',
        '-vframes', '1',
        thumbnail_path
    ]
    try:
        run_ffmpeg_command(cmd)
        relative_thumbnail_path = os.path.relpath(thumbnail_path, 'media/')
        instance.thumbnail = relative_thumbnail_path
        instance.thumbnail_created = True
        instance.save()
        logger.info(f'Thumbnail created and saved at {thumbnail_path}')
    except subprocess.CalledProcessError:
        logger.error(f'Failed to create thumbnail for {thumbnail_path} with error: {e}')
        raise
    

def set_thumbnail_path(video_path, is_global):
    if is_global:
        return video_path.replace('.mp4', '.jpg').replace('global_videos', 'global_thumbnails')
    else:
        return video_path.replace('.mp4', '.jpg').replace('local_videos', 'local_thumbnails')
    

def check_thumbnail_path(thumbnail_path):
    """
    Ensures the directory for the thumbnail path exists, creating it if necessary.

    Args:
        thumbnail_path (str): The full path where the thumbnail will be saved.
    """
    thumbnail_dir = os.path.dirname(thumbnail_path)
    if not os.path.exists(thumbnail_dir):
        try:
            os.makedirs(thumbnail_dir)
            logger.info(f'Directory created for thumbnail: {thumbnail_dir}')
        except OSError as e:
            logger.error(f'Failed to create directory {thumbnail_dir}: {e}')
            raise
        

def run_ffmpeg_command(cmd):
    """
    Runs the given ffmpeg command and logs the operation.

    Args:
        cmd (list): The command to run using subprocess.

    Raises:
        subprocess.CalledProcessError: If the ffmpeg command fails.
    """
    try:
        subprocess.run(cmd, check=True)
        logger.info(f'FFmpeg command executed successfully: {" ".join(cmd)}')
    except subprocess.CalledProcessError as e:
        logger.error(f'FFmpeg command failed: {" ".join(cmd)}; Error: {e}')
        raise