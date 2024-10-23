from unittest import mock
from app_videoflix.tasks import convert_720p

def test_convert_720p():
    # Testparameter
    source = "example_video.mp4"
    file_name = source.split('.')

    # Mocking der run_ffmpeg_command Funktion
    with mock.patch("app_videoflix.tasks.run_ffmpeg_command") as mock_run_ffmpeg_command:
        
        # Aufruf der convert_720p-Funktion
        convert_720p(source, file_name)
        
        # Erwarteter ffmpeg-Befehl
        expected_cmd = [
            'ffmpeg',
            '-i', source,
            '-s', 'hd720',
            '-c:v', 'libx264',
            '-crf', '23',
            '-c:a', 'aac',
            '-strict', '-2',
            'example_video_720p.mp4'
        ]
        
        # Überprüfen, ob run_ffmpeg_command mit dem richtigen Befehl aufgerufen wurde
        mock_run_ffmpeg_command.assert_called_once_with(expected_cmd)
