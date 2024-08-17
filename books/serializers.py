from rest_framework import serializers

from authors.serializers import AuthorBookSerializer, AuthorSerializer
from books.models import Book
from lendings.models import Lending
from lendings.serializers import LendingBookSerializer


class BookSerializer(serializers.ModelSerializer):
    """ Serializer для книги """
    class Meta:
        model = Book
        fields = ['title', 'author', 'text', 'year']


class BookListSerializer(serializers.ModelSerializer):
    """ Serializer для книги с подробным описанием автора """
    author_detail = AuthorSerializer(source='author')

    def get_fields(self):
        """ Если пользователь - библиотекарь, то добавляем поле "lendings", если пользователь -
        то удаляем поле "on_hand" """
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.user.groups.filter(name='librarian').exists():
            fields['lendings'] = serializers.SerializerMethodField()
        else:
            fields.pop('on_hand')
        return fields

    def get_lendings(self, obj):
        """ Получаем поле "lendings" """
        lendings = Lending.objects.filter(book=obj, active=True)
        serializer = LendingBookSerializer(lendings, many=True)
        return serializer.data

    class Meta:
        model = Book
        fields = '__all__'
