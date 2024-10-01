import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import GlobalVideo, LocalVideo


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='testpassword')

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