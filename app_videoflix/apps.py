from django.apps import AppConfig


class AppVideoflixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_videoflix'
    
    def ready(self):
        print("AppVideoflixConfig ready method called.")
        import app_videoflix.signals
