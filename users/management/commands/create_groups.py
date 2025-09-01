from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates user groups'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name='Moderator')
        self.stdout.write(self.style.SUCCESS('Successfully created groups'))
