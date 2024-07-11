from django.contrib import admin
from .models import GlobalVideo, LocalVideo

# Register your models here.
admin.site.register(GlobalVideo)
admin.site.register(LocalVideo)