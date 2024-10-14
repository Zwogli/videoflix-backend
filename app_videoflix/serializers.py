from rest_framework import serializers
from .models import GlobalVideo, LocalVideo

class GlobalVideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the GlobalVideo model.

    This serializer is responsible for converting GlobalVideo instances 
    into JSON format and vice versa. It includes all the fields relevant 
    for displaying global videos.
    """
    class Meta:
        model = GlobalVideo
        fields = ['id', 'title', 'description', 'thumbnail', 'file', 'is_local']


class LocalVideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the LocalVideo model.

    This serializer handles data conversion for LocalVideo instances, 
    including the user who uploaded the video and whether the video 
    is local or not.
    """
    class Meta:
        model = LocalVideo
        fields = ['id', 'title', 'description', 'thumbnail', 'file', 'uploaded_by', 'is_local']
        
        
class LocalVideoUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading local videos.

    This serializer handles the video upload process. It only includes 
    the required fields for uploading a video and excludes fields like 
    'uploaded_by', which are populated automatically in the view.
    """
    class Meta:
        model = LocalVideo
        fields = ['title', 'description', 'file']  # These fields are expected during upload

    def create(self, validated_data):
        """
        Create a new LocalVideo instance.

        This method saves a new LocalVideo object using the validated data provided.
        The 'uploaded_by' field will be handled in the view and passed separately.

        Args:
            validated_data (dict): The validated data for the new LocalVideo object.

        Returns:
            LocalVideo: The newly created LocalVideo instance.
        """
        return LocalVideo.objects.create(**validated_data)