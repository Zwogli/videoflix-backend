from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models.videos_global import GlobalVideo
from .models.videos_local import LocalVideo

# Register your models here.
class GlobalVideoResource(resources.ModelResource):

    class Meta:
        model = GlobalVideo
        

class LocalVideoResource(resources.ModelResource):

    class Meta:
        model = LocalVideo


@admin.register(GlobalVideo)
class GlobalVideoAdmin(ImportExportModelAdmin):
    resource_class = GlobalVideoResource
    
    
@admin.register(LocalVideo)
class LocalVideoAdmin(ImportExportModelAdmin):
    resource_class = LocalVideoResource