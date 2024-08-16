from datetime import timedelta

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import DAYS
from lendings.models import Lending
from lendings.serializers import LendingSerializer
from users.permissions import IsLibrarian


class LendingCreateAPIView(CreateAPIView):
    """ Создание выдачи """
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = (IsLibrarian,)

    def perform_create(self, serializer):
        """ Создание выдачи с проверкой наличия книг """
        with transaction.atomic():
            lending = serializer.save()
            lending.return_date = lending.lending_date + timedelta(days=DAYS)
            for book in lending.book.all():
                if book.on_hand:
                    raise serializers.ValidationError(
                        'Одна или несколько книг не в наличии проверьте правильность ввода данных'
                    )
                book.on_hand = True
                book.save()
            lending.save()


class LendingListAPIView(ListAPIView):
    """ Список выдач c фильтрацией """
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = (IsLibrarian,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'user']


class LendingRetrieveAPIView(RetrieveAPIView):
    """ Просмотр выдачи """
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = (IsLibrarian,)


class LendingActionAPIView(APIView):
    """ Возврат книги """
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = (IsLibrarian,)

    def post(self, request, pk):
        """ Метод возврата книги """
        lending = Lending.objects.get(pk=pk)
        lending.active = False
        lending.save()
        for book in lending.book.all():
            book.on_hand = False
            book.save()
        return Response('Книга(книги) возвращена(возвращены)', status=status.HTTP_200_OK)
