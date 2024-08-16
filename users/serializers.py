from rest_framework import serializers

from lendings.models import Lending

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Serializer для создания пользователя. """
    class Meta:
        model = User
        fields = '__all__'


class UserViewSerializer(serializers.ModelSerializer):
    """ Serializer для просмотра пользователя. """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'document', 'library_card', 'phone_number']


from lendings.serializers import LendingUserSerializer


class UserLibrarianViewSerializer(serializers.ModelSerializer):
    """ Serializer для просмотра пользователя (как библиотекарь). """
    lendings = serializers.SerializerMethodField()

    def get_lendings(self, obj):
        lendings = Lending.objects.filter(user=obj, active=True)
        serializer = LendingUserSerializer(lendings, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'library_card', 'phone_number', 'lendings']


class UserUpdateSerializer(serializers.ModelSerializer):
    """ Serializer для обновления пользователя. """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    """ Serializer для обновления пароля пользователя. """
    class Meta:
        model = User
        fields = ['password']
