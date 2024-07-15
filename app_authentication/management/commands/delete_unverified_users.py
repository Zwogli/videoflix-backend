from django.core.management.base import BaseCommand
from django.utils import timezone
from app_authentication.models import CustomUser

class Command(BaseCommand):
    help = 'Delete unverified users whose verification time has expired'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        unverified_users = CustomUser.objects.filter(is_verified=False, verification_expiry__lt=now)
        unverified_users.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted unverified users'))