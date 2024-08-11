from rest_framework import serializers

from authors.serializers import AuthorSerializer
from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'text', 'year']


class BookListSerializer(serializers.ModelSerializer):
    author_detail = AuthorSerializer(source='author')

    class Meta:
        model = Book
        fields = '__all__'
