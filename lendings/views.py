from datetime import timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from lendings.models import Lending
from lendings.serializers import LendingSerializer
from users.permissions import IsLibrarian


class LendingCreateAPIView(CreateAPIView):
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = (IsLibrarian,)

    def perform_create(self, serializer):
        lending = serializer.save()
        lending.return_date = lending.lending_date + timedelta(days=7)
        for book in lending.book.all():
            book.on_hand = True
            book.save()
        lending.save()

class LendingListAPIView(ListAPIView):
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = (IsLibrarian,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

class LendingRetrieveAPIView(RetrieveAPIView):
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = (IsLibrarian,)

class LendingActionAPIView(APIView):
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = (IsLibrarian,)

    def post(self, request, pk):
        lending = Lending.objects.get(pk=pk)
        lending.active = False
        lending.save()
        for book in lending.book.all():
            print(book)
            book.on_hand = False
            book.save()
        return Response('Книга(книги) возвращена(возвращены)', status=status.HTTP_200_OK)
