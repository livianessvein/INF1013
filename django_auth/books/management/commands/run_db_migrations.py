from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs makemigrations and migrate programmatically'

    def handle(self, *args, **options):
        self.stdout.write("Running makemigrations...")
        call_command('makemigrations')
        self.stdout.write("Running migrate...")
        call_command('migrate')
