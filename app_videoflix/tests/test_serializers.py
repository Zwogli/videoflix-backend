import pytest
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError
from ..models import GlobalVideo, LocalVideo
from ..serializers import GlobalVideoSerializer, LocalVideoSerializer, LocalVideoUploadSerializer
from app_authentication.models import CustomUser
from .utils import create_dummy_file


@pytest.mark.django_db
class TestGlobalVideoSerializer:
    def setup_method(self):
        self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')
        self.global_video = GlobalVideo.objects.create(
            title='Test Global Video',
            description='A test description for global video.',
            file='test_files/test_video.mp4',
            is_local=False
        )


    def test_global_video_serialization(self):
        serializer = GlobalVideoSerializer(self.global_video)
        data = serializer.data

        assert data['title'] == self.global_video.title
        assert data['description'] == self.global_video.description
        assert data['is_local'] == self.global_video.is_local
        assert 'file' in data  # Check whether the file field is present in the serialised data


@pytest.mark.django_db
class TestLocalVideoSerializer:
    def setup_method(self):
        self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')
        self.local_video = LocalVideo.objects.create(
            title='Test Local Video',
            description='A test description for local video.',
            uploaded_by=self.user,
            file='path/to/test_local_video.mp4',
            is_local=True
        )

    def test_local_video_serialization(self):
        serializer = LocalVideoSerializer(self.local_video)
        data = serializer.data

        assert data['title'] == self.local_video.title
        assert data['description'] == self.local_video.description
        assert data['is_local'] == self.local_video.is_local
        assert 'uploaded_by' in data  # Check whether the uploaded_by field is present in the data


@pytest.mark.django_db
class TestLocalVideoUploadSerializer:
    def setup_method(self):
        self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')

    def test_upload_serializer(self):
        uploaded_file = create_dummy_file(file_name='new_local_video.mp4')
        
        data = {
            'title': 'New Local Video',
            'description': 'Description of new local video',
            'file': uploaded_file 
        }
        serializer = LocalVideoUploadSerializer(data=data)
        # assert serializer.is_valid(), serializer.errors
        assert serializer.is_valid()  # Check whether the serialiser data is valid
        
        local_video = serializer.save(uploaded_by=self.user)  # Add user
        assert local_video.title == data['title']
        assert local_video.description == data['description']
        assert local_video.uploaded_by == self.user  # Check whether the user has been assigned
