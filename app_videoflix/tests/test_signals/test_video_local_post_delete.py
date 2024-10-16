import pytest
from unittest.mock import patch
from django.core.files.base import ContentFile
from app_authentication.models import CustomUser  # Importiere das benutzerdefinierte Benutzer-Modell
from app_videoflix.models import LocalVideo
from app_videoflix.signals import video_local_post_delete

@pytest.mark.django_db
class TestVideoLocalPostDelete:

    @pytest.fixture(autouse=True)
    def setup_video(self, db):
        # Erstelle einen Benutzer mit einer gültigen E-Mail und Benutzername
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            user_name='testuser',  # Der Benutzername wird hier korrekt gesetzt
            password='testpassword'
        )

        video_file_content = b'This is a test video file content.'
        video_file = ContentFile(video_file_content, name='local_video.mp4')
        
        # Erstelle das LocalVideo-Objekt
        self.video = LocalVideo(
            title='Test Local Video',
            file=video_file,
            uploaded_by=self.user,
        )
        self.video.save()

    @patch('app_videoflix.signals.delete_file')
    def test_video_local_post_delete(self, mock_delete_file):
        # Überprüfen, ob das Objekt korrekt gespeichert wurde
        assert LocalVideo.objects.count() == 1
        
        # Löschen des LocalVideo-Objekts
        self.video.delete()
        
        # Überprüfen, ob die delete_file-Funktion mit den richtigen Pfaden aufgerufen wurde
        video_path = self.video.file.path
        video_path_480p = video_path.replace('.mp4', '_480p.mp4')
        video_path_720p = video_path.replace('.mp4', '_720p.mp4')
        thumbnail_path = self.video.thumbnail.path if self.video.thumbnail else None
        
        # Erwartete Aufrufe an delete_file
        mock_delete_file.assert_any_call(video_path)
        mock_delete_file.assert_any_call(video_path_480p)
        mock_delete_file.assert_any_call(video_path_720p)
        if thumbnail_path:
            mock_delete_file.assert_any_call(thumbnail_path)

        # Überprüfen, ob das LocalVideo-Objekt gelöscht wurde
        assert LocalVideo.objects.count() == 0
