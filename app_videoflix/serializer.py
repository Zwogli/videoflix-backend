from rest_framework import serializers
from .models import GlobalVideo, LocalVideo

class GlobalVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalVideo
        fields = ['id', 'title', 'description', 'thumbnail', 'file']

class LocalVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalVideo
        fields = ['id', 'title', 'description', 'thumbnail', 'file', 'uploaded_by']