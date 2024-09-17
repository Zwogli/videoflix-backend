from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GlobalVideoViewSet, LocalVideoViewSet, UploadVideoView, thumbnail_status

router = DefaultRouter()    #todo definition
router.register(r'global-videos', GlobalVideoViewSet, basename='globalvideo')
router.register(r'local-videos', LocalVideoViewSet, basename='localvideo')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', UploadVideoView.as_view(), name='video-upload'),
    path('thumbnail-status/<int:video_id>/', thumbnail_status, name='thumbnail_status'),
]