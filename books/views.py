from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from pytils.translit import slugify
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import Author
from books.models import Book
from books.serializers import BookSerializer, BookListSerializer
from users.permissions import IsLibrarian


class BookCreateAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsLibrarian,)

    def perform_create(self, serializer):
        book = serializer.save()
        book.slug = slugify(book.title + '-' + str(book.pk))
        book.save()


class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug', 'author', 'year', 'on_hand']


class BookRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer


class BookUpdateAPIView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsLibrarian,)

    def perform_update(self, serializer):
        book = serializer.save()
        book.slug = slugify(book.title + '-' + str(book.pk))
        book.save()


class BookDeleteAPIView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsLibrarian,)


class BookSearchView(APIView):
    def post(self, request):
        query = str(request.data.get('query'))
        if query is None:
            return Response({'message': 'Заполните поле поиска'}, status=400)
        parts = query.split()
        q = Q()
        for i in parts:
            q |= Q(title__icontains=i) | Q(year__icontains=i) | Q(on_hand__icontains=i)
            books = Book.objects.filter(q)
            serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class SearchBookByAuthorView(APIView):
    def post(self, request):
        author_name = request.data.get('author_name')
        author_surname = request.data.get('author_surname')
        if author_name and author_surname:
            try:
                author = Author.objects.get(name__icontains=author_name, surname__icontains=author_surname)
            except Author.DoesNotExist:
                return Response({'message': 'Автор не найден'}, status=status.HTTP_404_NOT_FOUND)
        elif author_name:
            try:
                author = Author.objects.get(name__icontains=author_name)
            except Author.DoesNotExist:
                return Response(
                    {'message': 'Автор не найден или укажите поле "author_surname"'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif author_surname:
            try:
                author = Author.objects.get(surname__icontains=author_surname)
            except Author.DoesNotExist:
                return Response(
                    {'message': 'Автор не найден или укажите поле "author_name"'},
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {'message': 'Поля "author_name" и "author_surname" не заполнены'},
                status=status.HTTP_400_BAD_REQUEST
            )
        books = Book.objects.filter(author=author)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)
