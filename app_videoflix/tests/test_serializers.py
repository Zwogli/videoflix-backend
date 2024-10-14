# import pytest
# from rest_framework.exceptions import ValidationError
# from ..models import GlobalVideo, LocalVideo
# from ..serializers import GlobalVideoSerializer, LocalVideoSerializer, LocalVideoUploadSerializer
# from app_authentication.models import CustomUser

# @pytest.mark.django_db
# class TestGlobalVideoSerializer:
#     def setup_method(self):
#         self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')
#         self.global_video = GlobalVideo.objects.create(
#             title='Test Global Video',
#             description='A test description for global video.',
#             file='test_files/test_video.mp4',
#             is_local=False
#         )

#     def test_global_video_serialization(self):
#         serializer = GlobalVideoSerializer(self.global_video)
#         data = serializer.data

#         assert data['title'] == self.global_video.title
#         assert data['description'] == self.global_video.description
#         assert data['is_local'] == self.global_video.is_local
#         assert 'file' in data  # Überprüfe, ob das File-Feld in den serialisierten Daten vorhanden ist


# @pytest.mark.django_db
# class TestLocalVideoSerializer:
#     def setup_method(self):
#         self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')
#         self.local_video = LocalVideo.objects.create(
#             title='Test Local Video',
#             description='A test description for local video.',
#             uploaded_by=self.user,
#             file='path/to/test_local_video.mp4',
#             is_local=True
#         )

#     def test_local_video_serialization(self):
#         serializer = LocalVideoSerializer(self.local_video)
#         data = serializer.data

#         assert data['title'] == self.local_video.title
#         assert data['description'] == self.local_video.description
#         assert data['is_local'] == self.local_video.is_local
#         assert 'uploaded_by' in data  # Überprüfe, ob das uploaded_by-Feld in den Daten vorhanden ist


# @pytest.mark.django_db
# class TestLocalVideoUploadSerializer:
#     def setup_method(self):
#         self.user = CustomUser.objects.create_user(email='unique_test@mail.com', password='testpassword')

#     def test_upload_serializer(self):
#         data = {
#             'title': 'New Local Video',
#             'description': 'Description of new local video',
#             'file': 'path/to/new_video.mp4'  # Hier kann ebenfalls eine Dummy-Datei verwendet werden
#         }
#         serializer = LocalVideoUploadSerializer(data=data)
#         assert serializer.is_valid()  # Überprüfe, ob die Serializer-Daten gültig sind
        
#         local_video = serializer.save(uploaded_by=self.user)  # Füge den Benutzer hinzu
#         assert local_video.title == data['title']
#         assert local_video.description == data['description']
#         assert local_video.uploaded_by == self.user  # Überprüfe, ob der Benutzer zugewiesen wurde
