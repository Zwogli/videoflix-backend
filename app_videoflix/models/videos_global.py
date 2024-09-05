from django.db import models

class GlobalVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='global_videos/')
    thumbnail = models.ImageField(upload_to='global_thumbnails/', blank=True, null=True)
    is_local = models.BooleanField(default=False)

    def __str__(self):
        return self.title