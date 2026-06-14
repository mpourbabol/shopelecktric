from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Create deploy admin user when ADMIN_EMAIL and ADMIN_PASSWORD are set'

    def handle(self, *args, **options):
        import os

        email = os.environ.get('ADMIN_EMAIL', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '').strip()
        username = os.environ.get('ADMIN_USERNAME', 'admin').strip() or 'admin'

        if not email or not password:
            self.stdout.write('Skipping admin creation (ADMIN_EMAIL / ADMIN_PASSWORD not set).')
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(f'Admin user already exists: {email}')
            return

        User.objects.create_superuser(email=email, username=username, password=password)
        self.stdout.write(self.style.SUCCESS(f'Created admin user: {email}'))
