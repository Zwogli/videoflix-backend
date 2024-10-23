from app_videoflix.tasks import set_thumbnail_path

def test_set_thumbnail_path_global():
    video_path = "media/global_videos/example_video.mp4"
    is_global = True

    # Erwarteter Pfad für ein globales Video
    expected_thumbnail_path = "media/global_thumbnails/example_video.jpg"

    # Aufruf der Funktion
    result = set_thumbnail_path(video_path, is_global)

    # Überprüfen, ob der zurückgegebene Pfad korrekt ist
    assert result == expected_thumbnail_path


def test_set_thumbnail_path_local():
    video_path = "media/local_videos/example_video.mp4"
    is_global = False

    # Erwarteter Pfad für ein lokales Video
    expected_thumbnail_path = "media/local_thumbnails/example_video.jpg"

    # Aufruf der Funktion
    result = set_thumbnail_path(video_path, is_global)

    # Überprüfen, ob der zurückgegebene Pfad korrekt ist
    assert result == expected_thumbnail_path
