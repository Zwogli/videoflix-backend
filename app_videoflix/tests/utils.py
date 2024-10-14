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