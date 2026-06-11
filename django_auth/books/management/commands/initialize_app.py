from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs initialization'

    def handle(self, *args, **options):
        self.stdout.write("Running step 1...")
        call_command('makemigrations')
        self.stdout.write("Running step 2...")
        call_command('migrate')
