from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Create or update deploy admin from ADMIN_EMAIL and ADMIN_PASSWORD'

    def handle(self, *args, **options):
        import os

        email = os.environ.get('ADMIN_EMAIL', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '').strip()
        username = os.environ.get('ADMIN_USERNAME', 'admin').strip() or 'admin'

        if not email or not password:
            self.stdout.write('Skipping admin setup (ADMIN_EMAIL / ADMIN_PASSWORD not set).')
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'is_admin': True,
                'is_active': True,
            },
        )

        user.username = username
        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated admin password for: {email}'))
