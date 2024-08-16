from django.db import models
from django.utils import timezone

from books.models import Book
from users.models import User, NULLABLE


class Lending(models.Model):
    """Модель выдачи книги"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ManyToManyField(Book, verbose_name='Книга')
    lending_date = models.DateTimeField(default=timezone.now, verbose_name='Дата выдачи')
    return_date = models.DateTimeField(**NULLABLE, verbose_name='Дата возврата')
    active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        db_table = 'lendings'
        verbose_name = 'Выдача'
        verbose_name_plural = 'Выдачи'

    def __str__(self):
        return f'{self.user} - {self.active} - {self.lending_date}'
