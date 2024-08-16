from django.db import models

from users.models import NULLABLE


class Author(models.Model):
    """ Модель автора """
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    text = models.TextField(**NULLABLE, verbose_name='О авторе')
    slug = models.SlugField(unique=True, **NULLABLE, verbose_name='Ссылка')

    class Meta:
        db_table = 'authors'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.name} {self.surname}'
