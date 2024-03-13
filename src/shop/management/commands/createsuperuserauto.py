from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.settings import DJANGO_SUPER_ADMIN, DJANGO_SUPER_ADMIN_EMAIL, DJANGO_SUPER_ADMIN_PASSWORD


class Command(BaseCommand):
    help = "Creates a superuser with a predefined password and email"

    def handle(self, *args, **options):
        if User.objects.filter(username=DJANGO_SUPER_ADMIN).exists():
            self.stdout.write(self.style.WARNING("Superuser already exists"))
            return
        User.objects.create_superuser(DJANGO_SUPER_ADMIN, DJANGO_SUPER_ADMIN_EMAIL, DJANGO_SUPER_ADMIN_PASSWORD)
        self.stdout.write(self.style.SUCCESS("Successfully created a new superuser"))
