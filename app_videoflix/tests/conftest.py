import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from ..models import GlobalVideo, LocalVideo


@pytest.fixture(autouse=True)
def mock_redis():
    """Mock Redis connection for tests."""
    with patch('redis.StrictRedis') as mock_redis:
        mock_instance = mock_redis.return_value
        mock_instance.get.return_value = None  # Stelle sicher, dass Aufrufe zu Redis immer einen Mock-Wert zurückgeben
        yield mock_redis
        

@pytest.fixture(autouse=True)
def mock_rq():
    """Mock RQ connection for tests."""
    with patch('django_rq.get_queue') as mock_queue:
        yield mock_queue


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(email='unique_test@mail.com', password='testpassword')


@pytest.fixture
def global_video(db, user):
    video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
    return GlobalVideo.objects.create(
        title='Test Global Video',
        description='This is a test description for the global video.',
        file=video_file,  # A mock file is transferred here
    )


@pytest.fixture
def local_video(db, user):
    local_video_file = SimpleUploadedFile("test_local_video.mp4", b"file_content", content_type="video/mp4")
    return LocalVideo.objects.create(
        title='Test Local Video',
        description='This is a test description for the local video.',
        file=local_video_file,  # A mock file is transferred here
        uploaded_by=user,
    )
