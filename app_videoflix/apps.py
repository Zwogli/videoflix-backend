from django.apps import AppConfig
import logging


logger = logging.getLogger(__name__)


class AppVideoflixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_videoflix'
    
    def ready(self):
        logger.info("AppVideoflixConfig ready method called.")
        import app_videoflix.signals
