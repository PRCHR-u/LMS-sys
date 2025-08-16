from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    help = 'Clears migration history for users and admin apps.'

    def handle(self, *args, **options):
        with connections['default'].cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations WHERE app = 'users'")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'admin'")
        self.stdout.write(self.style.SUCCESS('Successfully cleared migration history for users and admin apps.'))