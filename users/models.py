from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    document = models.CharField(max_length=150, verbose_name='Документ')
    library_card = models.CharField(max_length=20, **NULLABLE, verbose_name='Номер библиотечной карточки')
    phone_number = models.CharField(max_length=20, **NULLABLE, verbose_name='Номер телефона')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.library_card} - {self.email}'

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
