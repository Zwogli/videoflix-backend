import subprocess
from .models import GlobalVideo, LocalVideo
import os


def convert(source):
    file_name = source.split('.')
    convert_480p(source, file_name)
    convert_720p(source, file_name)


def convert_480p(source, file_name):
    target = file_name[0] + '_480p.mp4'
    # cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    #{} sorce is set as a variable by the method .format(source, target)
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
    target = file_name[0] + '_720p.mp4'
    # cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    #{} sorce is set as a variable by the method .format(source, target)
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
    

def create_thumpnail(video_path, instance, is_global):
    thumbnail_path = set_thumpnail_path(video_path, is_global)
    check_thumpnail_path(thumbnail_path)    
        
    cmd = 'ffmpeg -i "{}" -ss 00:00:1.000 -vframes 1 "{}"'.format(video_path, thumbnail_path)
    subprocess.run(cmd)
    instance.thumbnail = thumbnail_path
    instance.save()
    

def set_thumpnail_path(video_path, is_global):
    if is_global:
        return video_path.replace('.mp4', '.jpg').replace('global_videos', 'global_thumbnails')
    else:
        return video_path.replace('.mp4', '.jpg').replace('local_videos', 'local_thumbnails')
    

def check_thumpnail_path(thumbnail_path):
    thumbnail_dir = os.path.dirname(thumbnail_path)
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir)