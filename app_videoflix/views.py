from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
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



@api_view(['GET'])
@permission_classes([AllowAny])
def thumbnail_status(request, video_id):
    """
    Check the thumbnail creation status of a local video and return the URL if created.
    """
    try:
        video = LocalVideo.objects.get(id=video_id)
        if video.thumbnail_created:
            # Verwende den Medien-URL-Pfad für das Thumbnail
            thumbnail_url = request.build_absolute_uri(f'/media/{video.thumbnail}')
            return Response({'thumbnailCreated': True, 'thumbnailUrl': thumbnail_url})
        else:
            return Response({'thumbnailCreated': False})
    except LocalVideo.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def thumbnail_status(request, video_id):
#     """
#     Check the thumbnail creation status of a local video.

#     This function returns whether the thumbnail for the video with the given ID 
#     has been created.

#     Args:
#         request: The HTTP request object.
#         video_id (int): The ID of the video to check.

#     Returns:
#         Response: A JSON response with the thumbnail creation status or an error message 
#         if the video does not exist.
#     """
#     try:
#         video = LocalVideo.objects.get(id=video_id)
#         return Response({'thumbnailCreated': video.thumbnail_created})
#     except LocalVideo.DoesNotExist:
#         # Handle case where the video doesn't exist and return a 404 response
#         return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)