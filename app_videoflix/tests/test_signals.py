from django.test import TestCase
from app_videoflix.signals import get_file_name_without_extension

class SignalTests(TestCase):

    def test_get_file_name_without_extension(self):
        video_path_with_extension = 'path/to/video/local_video.mp4'
        video_path_without_extension = 'path/to/video/local_video'

        file_name = get_file_name_without_extension(video_path_with_extension)

        self.assertEqual(file_name[0], 'path/to/video/local_video')

        # Teste einen Pfad ohne Erweiterung
        file_name_without_ext = get_file_name_without_extension(video_path_without_extension)
        self.assertEqual(file_name_without_ext[0], 'path/to/video/local_video')