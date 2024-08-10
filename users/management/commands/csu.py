import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания администратора
    """

    def handle(self, *args, **options):
        admin_user = User.objects.create(
            email=os.getenv('S_EMAIL'),
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        admin_user.set_password(os.getenv('S_PASSWORD'))
        admin_user.save()

        self.stdout.write(self.style.SUCCESS('Администратор создан'))
