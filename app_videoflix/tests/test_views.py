from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import GlobalVideo
from app_authentication.models import CustomUser
import io
from django.urls import reverse
from .utils import create_dummy_file


class GlobalVideoViewSetTests(APITestCase):
    def setUp(self):
        # Create admin-user
        self.admin_user = CustomUser.objects.create_superuser(
            email='admin@mail.com',
            password='testpassword'
        )

        uploaded_file = create_dummy_file(file_name='new_local_video.mp4')

        # Creates a global-video with dummy-data
        self.global_video = GlobalVideo.objects.create(
            title='Test Global Video',
            description='A test description for global video.',
            file=uploaded_file
        )

    def test_get_global_videos(self):
        self.client.login(email='admin@mail.com', password='testpassword')
        
        url = reverse('globalvideo-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.global_video.title)
