from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import status
from rest_framework.exceptions import PermissionDenied
# from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# from rest_framework.views import APIView

from users.models import User
from users.permissions import IsLibrarian
from users.serializers import UserSerializer, UserViewSerializer, UserLibrarianViewSerializer, UserUpdateSerializer, \
    UserPasswordUpdateSerializer
from users.services import generate_library_card_number


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.library_card = generate_library_card_number(user.id)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserLibrarianViewSerializer
    permission_classes = (IsLibrarian,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('library_card', 'phone_number', 'first_name', 'last_name')

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='librarian').exists():
            return UserLibrarianViewSerializer
        return UserSerializer

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True).exclude(groups__name='librarian')


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer

    def get_object(self):
        user = self.request.user
        pk = self.kwargs['pk']
        if pk != user.pk:
            raise PermissionDenied('Недостаточно прав для данного действия')
        return get_object_or_404(User, pk=pk)


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self):
        user = self.request.user
        pk = self.kwargs['pk']
        if pk != user.pk:
            raise PermissionDenied('Недостаточно прав для данного действия')
        return get_object_or_404(User, pk=pk)


class UserPasswordUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordUpdateSerializer

    def get_object(self):
        user = self.request.user
        pk = self.kwargs['pk']
        if pk != user.pk:
            raise PermissionDenied('Недостаточно прав для данного действия')
        return get_object_or_404(User, pk=pk)

    def partial_update(self, request, *args, **kwargs):
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


# class GetUserByDocumentView(APIView):
#     permission_classes = (IsLibrarian,)
#
#     def get(self, request, library_card):
#         try:
#             user = User.objects.get(library_card=library_card)
#             serializer = UserLibrarianViewSerializer(user)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
