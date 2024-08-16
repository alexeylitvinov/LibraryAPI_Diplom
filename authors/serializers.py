from rest_framework import serializers

from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """ Serializer для модели Автор. """
    def get_fields(self):
        """ При отображении списка авторов добавляем поле book_count и book_count_on_hand. """
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.user.groups.filter(name='librarian').exists():
            fields['book_count'] = serializers.IntegerField(source='book_set.count', read_only=True)
            fields['book_count_on_hand'] = serializers.SerializerMethodField()
        return fields

    def get_book_count_on_hand(self, author):
        """ Получаем поле book_count_on_hand. """
        return author.book_set.filter(on_hand=True).count()

    class Meta:
        model = Author
        fields = ['name', 'surname', 'text']


class AuthorBookSerializer(serializers.ModelSerializer):
    """ Serializer для модели Автор для добавления в serializer книг. """
    class Meta:
        model = Author
        fields = ['name', 'surname', 'text']
