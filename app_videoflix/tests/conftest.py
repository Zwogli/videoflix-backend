import pytest
from django.contrib.auth import get_user_model
from ..models import GlobalVideo, LocalVideo 

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def global_video(db, user):
    return GlobalVideo.objects.create(
        title='Test Global Video',
        user=user,
        # Setze hier weitere erforderliche Felder
    )

@pytest.fixture
def local_video(db, user):
    return LocalVideo.objects.create(
        title='Test Local Video',
        user=user,
        # Setze hier weitere erforderliche Felder
    )