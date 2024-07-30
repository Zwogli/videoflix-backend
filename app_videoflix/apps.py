from django.apps import AppConfig


class AppVideoflixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_videoflix'
    
    def ready(self):
        from . import signals
