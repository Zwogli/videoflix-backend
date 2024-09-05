from rest_framework import serializers
from .models import GlobalVideo, LocalVideo

class GlobalVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalVideo
        fields = ['id', 'title', 'description', 'thumbnail', 'file', 'is_local']

class LocalVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalVideo
        fields = ['id', 'title', 'description', 'thumbnail', 'file', 'uploaded_by', 'is_local']
        
        
class LocalVideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalVideo
        fields = ['title', 'description', 'file']  # Diese Felder werden erwartet

    def create(self, validated_data):
        # Erstellen und Speichern des neuen Videos
        return LocalVideo.objects.create(**validated_data)