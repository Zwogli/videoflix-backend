from django.shortcuts import render
from rest_framework import viewsets
from .models import GlobalVideo, LocalVideo
from .serializers import GlobalVideoSerializer, LocalVideoSerializer
from rest_framework.permissions import IsAuthenticated


class GlobalVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlobalVideo.objects.all()
    serializer_class = GlobalVideoSerializer


class LocalVideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocalVideoSerializer
    permission_classes = [IsAuthenticated]  # Ensures that the user must be authenticated to access the videos

    def get_queryset(self):
        # Only retrieve videos of the user currently logged in
        user = self.request.user  # Get the currently logged in user
        if user.is_staff:
            return LocalVideo.objects.all() 
        return LocalVideo.objects.filter(uploaded_by=user)


