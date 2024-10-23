import pytest
import subprocess
from unittest import mock
from app_videoflix.tasks import create_thumbnail

def test_create_thumbnail_success():
    video_path = "example_video.mp4"
    thumbnail_path = "example_thumbnail.jpg"
    instance = mock.Mock()  # Mock des Video-Modell-Objekts
    is_global = True

    # Mocking der abhängigen Funktionen
    with mock.patch("app_videoflix.tasks.set_thumbnail_path", return_value=thumbnail_path) as mock_set_thumbnail_path, \
         mock.patch("app_videoflix.tasks.check_thumbnail_path") as mock_check_thumbnail_path, \
         mock.patch("app_videoflix.tasks.run_ffmpeg_command") as mock_run_ffmpeg_command, \
         mock.patch("os.path.relpath", return_value="relative_thumbnail.jpg"), \
         mock.patch.object(instance, 'save') as mock_save:
        
        # Aufruf der Funktion
        create_thumbnail(video_path, instance, is_global)
        
        # Überprüfung, ob die Pfad-Funktionen korrekt aufgerufen wurden
        mock_set_thumbnail_path.assert_called_once_with(video_path, is_global)
        mock_check_thumbnail_path.assert_called_once_with(thumbnail_path)
        
        # Erwarteter ffmpeg-Befehl
        expected_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', '00:00:1.000',
            '-vframes', '1',
            thumbnail_path
        ]
        mock_run_ffmpeg_command.assert_called_once_with(expected_cmd)
        
        # Überprüfen, ob das instance-Objekt korrekt aktualisiert wurde
        assert instance.thumbnail == "relative_thumbnail.jpg"
        assert instance.thumbnail_created is True
        mock_save.assert_called_once()  # Überprüfen, ob instance.save() aufgerufen wurde

def test_create_thumbnail_ffmpeg_failure():
    video_path = "example_video.mp4"
    thumbnail_path = "example_thumbnail.jpg"
    instance = mock.Mock()
    is_global = True

    # Mocking der Funktionen und das Erzeugen eines Fehlers bei run_ffmpeg_command
    with mock.patch("app_videoflix.tasks.set_thumbnail_path", return_value=thumbnail_path), \
         mock.patch("app_videoflix.tasks.check_thumbnail_path"), \
         mock.patch("app_videoflix.tasks.run_ffmpeg_command", side_effect=subprocess.CalledProcessError(1, 'ffmpeg')), \
         mock.patch("os.path.relpath", return_value="relative_thumbnail.jpg"), \
         mock.patch.object(instance, 'save'):
        
        # Überprüfen, ob eine Exception ausgelöst wird, wenn ffmpeg fehlschlägt
        with pytest.raises(subprocess.CalledProcessError):
            create_thumbnail(video_path, instance, is_global)
        
        # Sicherstellen, dass save nicht aufgerufen wurde, wenn ffmpeg fehlschlägt
        instance.save.assert_not_called()
