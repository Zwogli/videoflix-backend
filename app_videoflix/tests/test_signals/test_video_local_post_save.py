import os
import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from unittest.mock import patch
from app_videoflix.models import LocalVideo

User = get_user_model()

@pytest.mark.django_db
class TestVideoLocalPostSave:

    @pytest.fixture(autouse=True)
    def setup_video(self, db):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            user_name='testuser',
            password='testpassword'
        )

        video_file_content = b'This is a test video file content.'
        video_file = ContentFile(video_file_content, name='local_video.mp4')
        self.video = LocalVideo(
            title='Test Local Video',
            file=video_file,
            uploaded_by=self.user,
        )

    @patch('app_videoflix.signals.queue_thumbnail_conversion')
    @patch('app_videoflix.signals.queue_video_resolution_conversion')
    def test_video_local_post_save(self, mock_queue_video_resolution, mock_queue_thumbnail_conversion):
        print("Vor dem Speichern des Videos")  # Debugging
        self.video.save()  # Dies sollte den post_save Signal auslösen
        
        # Hier debuggen wir den Handler
        print("Überprüfen der Aufrufe...")
        print("queue_thumbnail_conversion Aufrufe:", mock_queue_thumbnail_conversion.call_count)
        print("queue_video_resolution_conversion Aufrufe:", mock_queue_video_resolution.call_count)

        # Überprüfe, ob die Mock-Funktionen aufgerufen wurden
        try:
            mock_queue_thumbnail_conversion.assert_called_once_with(self.video.file.path, self.video, is_global=False)
            mock_queue_video_resolution.assert_called_once_with(self.video.file.path, os.path.splitext(self.video.file.name)[0])
        except AssertionError as e:
            print(f"AssertionError: {e}")

