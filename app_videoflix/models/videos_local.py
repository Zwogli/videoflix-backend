from django.db import models
from django.conf import settings

class LocalVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='local_videos/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='local_thumbnails/', blank=True, null=True)
    thumbnail_created = models.BooleanField(default=False)
    is_local = models.BooleanField(default=True)

    def __str__(self):
        return self.title