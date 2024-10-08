from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from pytils.translit import slugify
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import Author
from authors.serializers import AuthorSerializer
from books.paginations import CustomPagination
from users.permissions import IsLibrarian


class AuthorCreateAPIView(CreateAPIView):
    """ Создание автора """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsLibrarian,)

    def perform_create(self, serializer):
        """ Создание slug для автора """
        author = serializer.save()
        author.slug = slugify(author.__str__())
        author.save()


class AuthorListAPIView(ListAPIView):
    """ Список авторов c фильтром по slug """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('slug',)


class AuthorRetrieveAPIView(RetrieveAPIView):
    """ Просмотр автора """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsLibrarian,)


class AuthorUpdateAPIView(UpdateAPIView):
    """ Изменение автора """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsLibrarian,)

    def perform_update(self, serializer):
        """ Создание slug отредактированного автора """
        author = serializer.save()
        author.slug = slugify(author.__str__())
        author.save()


class AuthorDeleteAPIView(DestroyAPIView):
    """ Удаление автора """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsLibrarian,)


class AuthorSearchView(APIView):
    """ Поиск авторов """
    serializer_class = AuthorSerializer
    permission_classes = (IsLibrarian,)

    def post(self, request):
        """ Поиск авторов по имени и фамилии через Post запрос """
        query = request.data.get('query')
        if query is None:
            return Response({'message': 'Заполните поле поиска'}, status=400)
        parts = query.split()
        q = Q()
        for i in parts:
            q |= Q(name__icontains=i) | Q(surname__icontains=i)
            authors = Author.objects.filter(q)
            serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
