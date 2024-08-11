from rest_framework import serializers

from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(source='book_set.count', read_only=True)
    book_count_on_hand = serializers.SerializerMethodField()

    def get_book_count_on_hand(self, author):
        return author.book_set.filter(on_hand=True).count()

    class Meta:
        model = Author
        fields = ['name', 'surname', 'text', 'book_count', 'book_count_on_hand']
