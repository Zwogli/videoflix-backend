import subprocess


def convert_480p(source):
    file_name = source.split('.')
    target = file_name[0] + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    #{} sorce is set as a variable by the method .format(source, target)
    subprocess.run(cmd)