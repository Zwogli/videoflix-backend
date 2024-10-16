import io
from django.core.files.uploadedfile import InMemoryUploadedFile

def create_dummy_file(file_name='dummy_video.mp4', content=b'Test video content', content_type='video/mp4'):
    """
    Create a Dummy-file for tests.

    :param file_name: Your file-name
    :param content: Your file-content
    :param content_type: The MIME-Typ of the file
    :return: A InMemoryUploadedFile-object
    """
    file = io.BytesIO(content)
    file.name = file_name
    return InMemoryUploadedFile(file, None, file.name, content_type, file.getbuffer().nbytes, None)


def create_video_data(user, file_name='local_video.mp4'):
    """
    Create test data for creating a LocalVideo instance.

    :param user: The user who is uploading the video
    :param file_name: The name of the file to upload
    :return: A dictionary with video data
    """
    uploaded_file = create_dummy_file(file_name)
    return {
        'title': 'New Local Video',
        'description': 'Description of new local video',
        'file': uploaded_file,
        'uploaded_by': user.id
    }