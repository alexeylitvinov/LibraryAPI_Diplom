from django.db import models

from authors.models import Author
from users.models import NULLABLE


class Book(models.Model):
    """ Модель книги """
    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(**NULLABLE, verbose_name='О книге')
    genre = models.CharField(max_length=100, **NULLABLE, verbose_name='Жанр')
    slug = models.SlugField(unique=True, **NULLABLE, verbose_name='Ссылка')
    year = models.IntegerField(**NULLABLE, verbose_name='Год издания')
    on_hand = models.BooleanField(default=False, verbose_name='На руках')

    class Meta:
        db_table = 'books'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'{self.author} - {self.title}: {self.genre}'
