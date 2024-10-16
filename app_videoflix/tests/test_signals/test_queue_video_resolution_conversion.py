import pytest
from unittest.mock import patch
from app_videoflix.signals import queue_video_resolution_conversion
from app_videoflix.tasks import convert_480p, convert_720p

@pytest.mark.django_db
class VideoResolutionConversionTests:

    @patch('app_videoflix.signals.queue.enqueue')
    def test_queue_video_resolution_conversion(self, mock_enqueue):
        video_path = 'path/to/test_video.mp4'
        file_name = 'test_video.mp4'

        # Führe die Funktion aus
        queue_video_resolution_conversion(video_path, file_name)

        # Überprüfe, ob die Warteschlange korrekt aufgerufen wurde
        mock_enqueue.assert_any_call(convert_480p, video_path, file_name)
        mock_enqueue.assert_any_call(convert_720p, video_path, file_name)

        # Überprüfe, dass die Warteschlange genau zweimal aufgerufen wurde
        assert mock_enqueue.call_count == 2
