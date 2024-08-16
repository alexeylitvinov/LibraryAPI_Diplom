from rest_framework import serializers

from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    # book_count = serializers.IntegerField(source='book_set.count', read_only=True)
    # book_count_on_hand = serializers.SerializerMethodField()
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.user.groups.filter(name='librarian').exists():
            fields['book_count'] = serializers.IntegerField(source='book_set.count', read_only=True)
            fields['book_count_on_hand'] = serializers.SerializerMethodField()
        return fields

    def get_book_count_on_hand(self, author):
        return author.book_set.filter(on_hand=True).count()

    class Meta:
        model = Author
        fields = ['name', 'surname', 'text']


class AuthorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'text']
