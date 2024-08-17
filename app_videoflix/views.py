from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import GlobalVideo, LocalVideo
from .serializers import GlobalVideoSerializer, LocalVideoSerializer, LocalVideoUploadSerializer
from rest_framework.permissions import IsAuthenticated


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class GlobalVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlobalVideo.objects.all()
    serializer_class = GlobalVideoSerializer


# @method_decorator(cache_page(CACHE_TTL), name='dispatch')
class LocalVideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocalVideoSerializer
    permission_classes = [IsAuthenticated]  # Ensures that the user must be authenticated to access the videos

    def get_queryset(self):
        # Only retrieve videos of the user currently logged in
        user = self.request.user  # Get the currently logged in user
        if user.is_staff:
            return LocalVideo.objects.all() 
        return LocalVideo.objects.filter(uploaded_by=user)
    

class UploadVideoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = LocalVideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)  # Saving the video with the currently logged in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


