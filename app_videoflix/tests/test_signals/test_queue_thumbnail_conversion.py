import pytest
from django.core.files.base import ContentFile 
from unittest.mock import patch
from app_authentication.models import CustomUser
from app_videoflix.models import LocalVideo
from app_videoflix.signals import queue_thumbnail_conversion
from app_videoflix.tasks import create_thumbnail


@pytest.mark.django_db  # Stelle sicher, dass die Tests auf die Datenbank zugreifen können
class ThumbnailConversionTests:

    @pytest.fixture(autouse=True)
    def setup_user(self, db):  # Fixture zum Einrichten eines Benutzers
        self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')

    @patch('app_videoflix.signals.queue.enqueue')  # Mock der Warteschlange
    def test_queue_thumbnail_conversion(self, mock_enqueue, caplog):
        video_file_content = b'This is a test video file content.'
        video_file = ContentFile(video_file_content, name='local_video.mp4')

        # Erstelle eine LocalVideo-Instanz mit dem Mock-Dateiinhalt
        local_video = LocalVideo.objects.create(
            title='Test Local Video',
            description='This is a test description for the local video.',
            file=video_file,
            uploaded_by=self.user,
        )

        video_path = local_video.file.path  # Erhalte den Pfad zur Video-Datei
        is_global = False

        # Führe die Funktion aus und logge die Informationen
        with caplog.at_level('INFO'):
            queue_thumbnail_conversion(video_path, local_video, is_global)

        # Überprüfe, ob die Warteschlange korrekt aufgerufen wurde
        mock_enqueue.assert_called_once_with(create_thumbnail, video_path, local_video, is_global)

        # Überprüfe, ob das Logging erfolgt ist
        assert 'Thumbnail creation task enqueued for' in caplog.text

    @patch('app_videoflix.signals.queue.enqueue')
    def test_queue_thumbnail_conversion_failure(self, mock_enqueue, caplog):
        # Simuliere einen Fehler beim Enqueue
        mock_enqueue.side_effect = Exception('Enqueue failed')

        video_file_content = b'This is a test video file content.'
        video_file = ContentFile(video_file_content, name='local_video.mp4')

        local_video = LocalVideo.objects.create(
            title='Test Local Video',
            description='This is a test description for the local video.',
            file=video_file,
            uploaded_by=self.user,
        )

        video_path = local_video.file.path  # Erhalte den Pfad zur Video-Datei
        is_global = False

        # Führe die Funktion aus und logge die Informationen
        with caplog.at_level('ERROR'):
            queue_thumbnail_conversion(video_path, local_video, is_global)

        # Überprüfe, ob der Fehler geloggt wurde
        assert 'Failed to enqueue thumbnail creation for video:' in caplog.text