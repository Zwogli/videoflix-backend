"""
import pytest
from ..models import GlobalVideo, LocalVideo


def test_create_global_video(global_video):
    assert global_video.id is not None
    assert global_video.title == 'Test Global Video'
    assert global_video.description == 'Test description'
    assert global_video.is_local is False

def test_create_local_video(local_video):
    assert local_video.id is not None
    assert local_video.title == 'Test Local Video'
    assert local_video.description == 'Test description'
    assert local_video.uploaded_by is not None
    assert local_video.is_local is True

def test_global_video_str(global_video):
    assert str(global_video) == 'Test Global Video'

def test_local_video_str(local_video):
    assert str(local_video) == 'Test Local Video'

def test_file_upload(global_video):
    assert global_video.file.name == 'global_videos/test_video.mp4'

def test_file_upload_local_video(local_video):
    assert local_video.file.name == 'local_videos/test_local_video.mp4'
"""