from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import GlobalVideo, LocalVideo
from app_authentication.models import CustomUser
import io
from django.urls import reverse
from .utils import create_dummy_file, create_video_data


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
        
        
class LocalVideoViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='user@mail.com', password='testpassword')
        self.admin_user = CustomUser.objects.create_superuser(email='admin@mail.com', password='adminpassword')

        self.client.login(email='user@mail.com', password='testpassword')


    def test_create_local_video(self):
        url = reverse('localvideo-list')
        data = create_video_data(self.user)
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LocalVideo.objects.count(), 1)
        self.assertEqual(LocalVideo.objects.get().title, 'New Local Video')


    def test_get_local_videos(self):
        uploaded_file = create_dummy_file(file_name='local_video.mp4')
        LocalVideo.objects.create(title='Local Video', description='Test video', uploaded_by=self.user, file=uploaded_file)

        url = reverse('localvideo-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Local Video')


    def test_update_local_video(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        uploaded_file = create_dummy_file(file_name='local_video.mp4')
        local_video = LocalVideo.objects.create(
            title='Old Title', 
            description='Test video', 
            uploaded_by=self.user, 
            file=uploaded_file
        )

        # Update only title and discription
        url = reverse('localvideo-detail', args=[local_video.id])
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
        }

        response = client.patch(url, data, format='json')  # For text-updates use JSON-format

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        local_video.refresh_from_db()
        self.assertEqual(local_video.title, 'Updated Title')
        self.assertEqual(local_video.description, 'Updated description')


    def test_delete_local_video(self):
        uploaded_file = create_dummy_file(file_name='local_video.mp4')
        local_video = LocalVideo.objects.create(title='Video to delete', description='Test video', uploaded_by=self.user, file=uploaded_file)

        url = reverse('localvideo-detail', args=[local_video.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(LocalVideo.objects.count(), 0)
