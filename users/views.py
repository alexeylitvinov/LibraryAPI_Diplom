from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.permissions import IsLibrarian
from users.serializers import UserSerializer, UserViewSerializer, UserLibrarianViewSerializer, UserUpdateSerializer, \
    UserPasswordUpdateSerializer
from users.services import generate_library_card_number


class UserCreateAPIView(CreateAPIView):
    """ Создание пользователя """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """ Создание пользователя с кешированием пароля """
        user = serializer.save(is_active=True)
        user.library_card = generate_library_card_number(user.id)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """ Список пользователей """
    serializer_class = UserLibrarianViewSerializer
    permission_classes = (IsLibrarian,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('library_card', 'phone_number', 'first_name', 'last_name')

    def get_queryset(self):
        """ Исключаем суперпользователя и группу "librarian" из списка """
        return User.objects.exclude(is_superuser=True).exclude(groups__name='librarian')


class UserRetrieveAPIView(RetrieveAPIView):
    """ Просмотр пользователя """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """ Определяем какой сериализатор использовать для данного запроса """
        if self.request.user.groups.filter(name='librarian').exists():
            return UserLibrarianViewSerializer
        return UserViewSerializer

    def get_object(self):
        """ Получаем пользователя и проверяем права доступа """
        user = self.request.user
        pk = self.kwargs['pk']
        if user.groups.filter(name='librarian').exists():
            return get_object_or_404(User, pk=pk)
        elif pk != user.pk:
            raise PermissionDenied('Недостаточно прав для данного действия')
        return get_object_or_404(User, pk=pk)


class UserUpdateAPIView(UpdateAPIView):
    """ Обновление пользователя """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self):
        """ Получаем пользователя и проверяем права доступа """
        user = self.request.user
        pk = self.kwargs['pk']
        if pk != user.pk:
            raise PermissionDenied('Недостаточно прав для данного действия')
        return get_object_or_404(User, pk=pk)


class UserPasswordUpdateAPIView(UpdateAPIView):
    """ Класс обновления пароля пользователя """
    queryset = User.objects.all()
    serializer_class = UserPasswordUpdateSerializer

    def get_object(self):
        """ Получаем пользователя и проверяем права доступа """
        user = self.request.user
        pk = self.kwargs['pk']
        if pk != user.pk:
            raise PermissionDenied('Недостаточно прав для данного действия')
        return get_object_or_404(User, pk=pk)

    def partial_update(self, request, *args, **kwargs):
        """ Обновление пароля пользователя """
        user = self.get_object()
        if 'password' in request.data:
            password = request.data.get('password')
            if password is not None:
                user.set_password(str(password))
                user.save()
                return Response({'message': 'Пароль успешно обновлен'})
            else:
                return Response({'message': 'Заполните поле пароля'}, status=400)
        else:
            return Response({'message': 'Заполните поле пароля'}, status=400)
