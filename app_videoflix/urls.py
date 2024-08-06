from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GlobalVideoViewSet, LocalVideoViewSet

router = DefaultRouter()    #todo definition
router.register(r'global-videos', GlobalVideoViewSet, basename='globalvideo')
router.register(r'local-videos', LocalVideoViewSet, basename='localvideo')

urlpatterns = [
    path('', include(router.urls)),
]