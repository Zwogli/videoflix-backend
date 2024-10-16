import os
import pytest
from django.core.files.base import ContentFile
from unittest.mock import patch
from app_authentication.models import CustomUser
from app_videoflix.models import GlobalVideo


@pytest.mark.django_db
class TestVideoGlobalPostDelete:

    @pytest.fixture(autouse=True)
    def setup_user_and_video(self, db):
        # Erstelle einen Benutzer
        self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')
        
        # Erstelle eine GlobalVideo-Instanz
        video_file_content = b'This is a test video file content.'
        video_file = ContentFile(video_file_content, name='global_video.mp4')
        self.video = GlobalVideo.objects.create(
            title='Test Global Video',
            file=video_file,
            thumbnail=None  # Oder füge eine Thumbnail-Datei hinzu, wenn erforderlich
        )

    @patch('app_videoflix.signals.delete_file')  # Mock der delete_file-Funktion
    def test_video_global_post_delete(self, mock_delete_file):
        # Lösche das GlobalVideo-Objekt
        self.video.delete()
        
        # Überprüfe, ob die delete_file-Funktion mit den richtigen Pfaden aufgerufen wurde
        video_path = self.video.file.path
        video_path_480p = video_path.replace('.mp4', '_480p.mp4')
        video_path_720p = video_path.replace('.mp4', '_720p.mp4')
        
        mock_delete_file.assert_any_call(video_path)
        mock_delete_file.assert_any_call(video_path_480p)
        mock_delete_file.assert_any_call(video_path_720p)
        mock_delete_file.assert_any_call(None)  # Wenn kein Thumbnail vorhanden ist
        
        # Optionale Bestätigung, dass die Mock-Funktion auch genau einmal aufgerufen wurde
        assert mock_delete_file.call_count == 4
