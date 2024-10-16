import pytest
from django.core.files.base import ContentFile
from unittest.mock import patch
from app_videoflix.signals import get_file_name_without_extension
from app_videoflix.models import GlobalVideo
from app_authentication.models import CustomUser
from app_videoflix.signals import queue_thumbnail_conversion, queue_video_resolution_conversion


@pytest.mark.django_db
class GlobalVideoSignalTests:

    @pytest.fixture(autouse=True)
    def setup_user(self, db):
        self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')

    @patch('app_videoflix.signals.queue.enqueue')
    @patch('app_videoflix.signals.logger')
    def test_video_global_post_save_creates_tasks(self, mock_logger, mock_enqueue):
        # Erstelle ein GlobalVideo-Objekt
        video_file_content = b'This is a test global video file content.'
        video_file = ContentFile(video_file_content, name='global_video.mp4')

        global_video = GlobalVideo.objects.create(
            title='Test Global Video',
            description='This is a test description for the global video.',
            file=video_file,
            uploaded_by=self.user,
        )

        # Überprüfe, ob die Logging-Nachricht generiert wurde
        mock_logger.info.assert_called_with('New global video created: %s', global_video.file.name)

        # Überprüfe, ob die Thumbnail- und Video-Konvertierungsaufgaben eingereiht wurden
        video_path = global_video.file.path
        file_name = get_file_name_without_extension(video_path)

        queue_thumbnail_conversion.assert_called_once_with(video_path, global_video, is_global=True)
        queue_video_resolution_conversion.assert_called_once_with(video_path, file_name)

    @patch('app_videoflix.signals.logger')
    def test_video_global_post_save_update(self, mock_logger):
        # Erstelle ein GlobalVideo-Objekt
        video_file_content = b'This is a test global video file content.'
        video_file = ContentFile(video_file_content, name='global_video.mp4')

        global_video = GlobalVideo.objects.create(
            title='Test Global Video',
            description='This is a test description for the global video.',
            file=video_file,
            uploaded_by=self.user,
        )

        # Aktualisiere das GlobalVideo-Objekt
        global_video.title = 'Updated Global Video'
        global_video.save()  # Dies sollte die 'else'-Bedingung auslösen

        # Überprüfe, ob die Logging-Nachricht für das Update generiert wurde
        mock_logger.info.assert_called_with('Global video updated: %s', global_video.file.name)
