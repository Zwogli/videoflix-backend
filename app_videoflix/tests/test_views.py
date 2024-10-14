"""
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import GlobalVideo
from app_authentication.models import CustomUser
import io


class GlobalVideoViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')

        # Simuliere eine Datei für den Upload
        file = io.BytesIO(b'Test video content')  # Erstelle einen BytesIO-Stream
        file.name = 'test_video.mp4'  # Setze den Dateinamen
        uploaded_file = InMemoryUploadedFile(file, None, file.name, 'video/mp4', file.getbuffer().nbytes, None)

        # Erstelle das GlobalVideo-Objekt mit der simulierten Datei
        self.global_video = GlobalVideo.objects.create(
            title='Test Global Video',
            description='A test description for global video.',
            file=uploaded_file  # Setze die Datei
        )

    def test_get_global_videos(self):
        url = reverse('globalvideo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.global_video.title)
"""