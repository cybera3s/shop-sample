from django.core.checks import database
from django.core.management.base import BaseCommand
from accounts.models import OtpCode

from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'remove all expired otp codes'

    def handle(self, *args, **options):
        expire_time = timezone.now() - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expire_time).delete()
        self.stdout.write(self.style.SUCCESS('successfully removed expired otp'))
