from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import GlobalVideo, LocalVideo
from .serializers import GlobalVideoSerializer, LocalVideoSerializer, LocalVideoUploadSerializer
from rest_framework.permissions import IsAuthenticated


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class GlobalVideoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing global videos.

    This viewset allows only read-only access to global videos.

    Attributes:
        queryset: The list of GlobalVideo objects that are returned.
        serializer_class: The serializer used to format GlobalVideo data.
    """
    queryset = GlobalVideo.objects.all()
    serializer_class = GlobalVideoSerializer
    permission_classes = [AllowAny]


class LocalVideoViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing local videos.

    This viewset allows authenticated users to create, retrieve, update, 
    and delete local videos. Non-staff users can only see their own videos.
    """
    serializer_class = LocalVideoSerializer
    permission_classes = [IsAuthenticated]  # Ensures that the user must be authenticated to access the videos

    def get_queryset(self):
        user = self.request.user  # Get the current user making the request
        
        # If the user is an admin (staff), return all local videos
        if user.is_staff: 
            return LocalVideo.objects.all()
        
        # Otherwise, return only the videos uploaded by the current user
        return LocalVideo.objects.filter(uploaded_by=user)
    

class UploadVideoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for uploading local videos.

        This method processes the video upload request, validates it using the 
        LocalVideoUploadSerializer, and assigns the current logged-in user as the uploader.

        Args:
            request: The HTTP request object containing the video data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response object containing the serializer data if successful, 
            or the validation errors if not.
        """
        serializer = LocalVideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)  # Saving the video with the currently logged in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" Test polling
@api_view(['GET'])
def thumbnail_status(request):
    videos = LocalVideoSerializer.objects.filter(is_local=True)
    serializer = LocalVideoSerializer(videos, many=True)
    return Response(serializer.data)
"""


@api_view(['GET'])
@permission_classes([AllowAny])
def thumbnail_status(request, video_id):
    """
    Check the thumbnail creation status of a local video.

    This function returns whether the thumbnail for the video with the given ID 
    has been created.

    Args:
        request: The HTTP request object.
        video_id (int): The ID of the video to check.

    Returns:
        Response: A JSON response with the thumbnail creation status or an error message 
        if the video does not exist.
    """
    try:
        video = LocalVideo.objects.get(id=video_id)
        return Response({'thumbnailCreated': video.thumbnail_created})
    except LocalVideo.DoesNotExist:
        # Handle case where the video doesn't exist and return a 404 response
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def thumbnail_status_test(request, video_id):
    """
    API-Endpunkt, um den Status der Thumbnail-Generierung abzufragen.
    """
    base_url = settings.BASE_URL
    video = get_object_or_404(LocalVideo, id=video_id)
    
    if video.thumbnail_created:
        thumbnail_url = f"{base_url}{video.thumbnail.url}" if video.thumbnail else None
        return Response({
            "status": "done",
            "thumbnail_url": thumbnail_url
        })
    else:
        return Response({
            "status": "pending",
            "thumbnail_url": None
        })