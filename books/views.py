from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from pytils.translit import slugify
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import Author
from books.models import Book
from books.paginations import CustomPagination
from books.serializers import BookSerializer, BookListSerializer
from users.permissions import IsLibrarian


class BookCreateAPIView(CreateAPIView):
    """ Создание книги """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsLibrarian,)

    def perform_create(self, serializer):
        """ Создание slug книги """
        book = serializer.save()
        book.slug = slugify(book.title + '-' + str(book.pk))
        book.save()


class BookListAPIView(ListAPIView):
    """ Просмотр книг с фильтрацией """
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug', 'title', 'genre', 'author', 'year', 'on_hand']

    def get_queryset(self):
        """ Для библиотекаря выбираются все книги, для пользователя - только книги у которых on_hand = False """
        if self.request.user.groups.filter(name='librarian').exists():
            return Book.objects.all()
        else:
            return Book.objects.filter(on_hand=False)


class BookRetrieveAPIView(RetrieveAPIView):
    """ Просмотр конкретной книги """
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

    def get_queryset(self):
        """ Для библиотекаря выбираются все книги, для пользователя - только книги у которых on_hand = False """
        if self.request.user.groups.filter(name='librarian').exists():
            return Book.objects.all()
        else:
            return Book.objects.filter(on_hand=False)


class BookUpdateAPIView(UpdateAPIView):
    """ Изменение книги """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsLibrarian,)

    def perform_update(self, serializer):
        """ Создание slug отредактированной книги """
        book = serializer.save()
        book.slug = slugify(book.title + '-' + str(book.pk))
        book.save()


class BookDeleteAPIView(DestroyAPIView):
    """ Удаление книги """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsLibrarian,)


class BookSearchView(APIView):
    """ Поиск книг по названию, жанру или наличию на руках через Post запрос """
    permission_classes = (IsLibrarian,)

    def post(self, request):
        """ Реализация поиска по названию, жанру или наличию на руках """
        query = str(request.data.get('query'))
        if query is None:
            return Response({'message': 'Заполните поле поиска'}, status=400)
        parts = query.split()
        q = Q()
        for i in parts:
            q |= Q(title__icontains=i) | Q(genre__icontains=i) | Q(on_hand__icontains=i)
            books = Book.objects.filter(q)
            serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class SearchBookByAuthorView(APIView):
    """ Поиск книг по автору через Post запрос """
    permission_classes = (IsLibrarian,)

    def post(self, request):
        """ Реализация поиска по автору """
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
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)
