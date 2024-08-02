import subprocess
from .models import GlobalVideo, LocalVideo


def convert(source):
    file_name = source.split('.')
    convert_480p(source, file_name)
    convert_720p(source, file_name)


def convert_480p(source, file_name):
    target = file_name[0] + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    #{} sorce is set as a variable by the method .format(source, target)
    subprocess.run(cmd)
    
    
def convert_720p(source, file_name):
    target = file_name[0] + '_720p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd7200 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    #{} sorce is set as a variable by the method .format(source, target)
    subprocess.run(cmd)
    

def createThumpnail(video_path, instance):
    thumbnail_path = video_path.replace('.mp4', '.jpg')
    cmd = 'ffmpeg -i "{}" -ss 00:00:1.000 -vframes 1 "{}"'.format(video_path, thumbnail_path)
    subprocess.run(cmd)
    instance.thumbnail = thumbnail_path
    instance.save()