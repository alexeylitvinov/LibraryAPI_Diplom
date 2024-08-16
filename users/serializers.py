from rest_framework import serializers

from lendings.models import Lending

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'document', 'library_card', 'phone_number']


from lendings.serializers import LendingUserSerializer


class UserLibrarianViewSerializer(serializers.ModelSerializer):
    lendings = serializers.SerializerMethodField()

    def get_lendings(self, obj):
        lendings = Lending.objects.filter(user=obj, active=True)
        serializer = LendingUserSerializer(lendings, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'library_card', 'phone_number', 'lendings']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
