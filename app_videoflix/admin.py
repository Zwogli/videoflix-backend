from django.contrib import admin
from .models.videos_global import GlobalVideo
from .models.videos_local import LocalVideo

# Register your models here.
admin.site.register(GlobalVideo)
admin.site.register(LocalVideo)