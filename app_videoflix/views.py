from django.shortcuts import render
from rest_framework import viewsets
from .models import GlobalVideo, LocalVideo
from .serializers import GlobalVideoSerializer, LocalVideoSerializer


class GlobalVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlobalVideo.objects.all()
    serializer_class = GlobalVideoSerializer


class LocalVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LocalVideo.objects.all()
    serializer_class = LocalVideoSerializer


