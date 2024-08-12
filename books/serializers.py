from rest_framework import serializers

from authors.serializers import AuthorBookSerializer
from books.models import Book
from lendings.models import Lending
from lendings.serializers import LendingBookSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'text', 'year']


class BookListSerializer(serializers.ModelSerializer):
    author_detail = AuthorBookSerializer(source='author')
    lendings = serializers.SerializerMethodField()

    def get_lendings(self, obj):
        lendings = Lending.objects.filter(book=obj, active=True)
        serializer = LendingBookSerializer(lendings, many=True)
        return serializer.data

    class Meta:
        model = Book
        fields = '__all__'
