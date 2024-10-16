from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from app_videoflix.models import LocalVideo
from app_authentication.models import CustomUser
from app_videoflix.tests.utils import create_dummy_file, get_video_upload_data


class UploadVideoViewTests(APITestCase):
    def setUp(self):
        # Create a user and authenticate the client
        self.user = CustomUser.objects.create_user(email='user@mail.com', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_upload_video(self):
        """
        Test uploading a new video via the UploadVideoView.
        """
        uploaded_file = create_dummy_file(file_name='test_video.mp4')
        data = get_video_upload_data(uploaded_file)
        
        url = reverse('video-upload')
        response = self.client.post(url, data, format='multipart')

        if response.status_code != status.HTTP_201_CREATED:
            print('Test response data:', response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LocalVideo.objects.count(), 1)
        uploaded_video = LocalVideo.objects.get()
        self.assertEqual(uploaded_video.title, 'Test Video')
        self.assertEqual(uploaded_video.uploaded_by, self.user)