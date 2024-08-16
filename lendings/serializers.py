from rest_framework import serializers

from lendings.models import Lending
from users.serializers import UserViewSerializer


class LendingSerializer(serializers.ModelSerializer):
    """ Serializer для модели выдачи книг. """
    lending_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    return_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    user_detail = serializers.SerializerMethodField()

    def get_user_detail(self, obj):
        """ Возвращает данные пользователя для вложенного поля user_detail. """
        return UserViewSerializer(obj.user).data

    class Meta:
        model = Lending
        fields = '__all__'


class LendingUserSerializer(serializers.ModelSerializer):
    """ Serializer для модели выдачи книг. Используется для сериализации данных пользователя. """
    lending_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    return_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Lending
        fields = ['id', 'book', 'lending_date', 'return_date']


class LendingBookSerializer(serializers.ModelSerializer):
    """ Serializer для модели выдачи книг. Используется для сериализации данных книги. """
    lending_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    return_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Lending
        fields = ['id', 'user', 'lending_date', 'return_date']
