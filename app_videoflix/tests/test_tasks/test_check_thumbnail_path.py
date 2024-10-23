import os
import pytest
from unittest import mock
from app_videoflix.tasks import check_thumbnail_path

def test_check_thumbnail_path_directory_exists():
    thumbnail_path = "media/global_thumbnails/example_video.jpg"
    thumbnail_dir = os.path.dirname(thumbnail_path)

    # Simuliere, dass das Verzeichnis bereits existiert
    with mock.patch("os.path.exists", return_value=True) as mock_exists:
        with mock.patch("os.makedirs") as mock_makedirs:
            check_thumbnail_path(thumbnail_path)
            
            # Überprüfe, dass makedirs nicht aufgerufen wurde, weil das Verzeichnis existiert
            mock_exists.assert_called_once_with(thumbnail_dir)
            mock_makedirs.assert_not_called()

def test_check_thumbnail_path_directory_does_not_exist():
    thumbnail_path = "media/global_thumbnails/example_video.jpg"
    thumbnail_dir = os.path.dirname(thumbnail_path)

    # Simuliere, dass das Verzeichnis nicht existiert
    with mock.patch("os.path.exists", return_value=False) as mock_exists:
        with mock.patch("os.makedirs") as mock_makedirs:
            check_thumbnail_path(thumbnail_path)

            # Überprüfe, dass makedirs aufgerufen wurde, um das Verzeichnis zu erstellen
            mock_exists.assert_called_once_with(thumbnail_dir)
            mock_makedirs.assert_called_once_with(thumbnail_dir)

def test_check_thumbnail_path_makedirs_failure():
    thumbnail_path = "media/global_thumbnails/example_video.jpg"
    thumbnail_dir = os.path.dirname(thumbnail_path)

    # Simuliere, dass das Verzeichnis nicht existiert
    with mock.patch("os.path.exists", return_value=False) as mock_exists:
        # Simuliere, dass os.makedirs eine OSError auslöst
        with mock.patch("os.makedirs", side_effect=OSError("Failed to create directory")) as mock_makedirs:
            with mock.patch("app_videoflix.tasks.logger.error") as mock_logger:
                with pytest.raises(OSError, match="Failed to create directory"):
                    check_thumbnail_path(thumbnail_path)

                # Überprüfe, dass der Logger einen Fehler protokolliert hat
                mock_logger.assert_called_once_with(f'Failed to create directory {thumbnail_dir}: Failed to create directory')
                mock_makedirs.assert_called_once_with(thumbnail_dir)
