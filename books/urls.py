from django.urls import path

from books.apps import BooksConfig
from books.views import BookCreateAPIView, BookListAPIView, BookRetrieveAPIView, BookUpdateAPIView, BookDeleteAPIView, \
    BookSearchView, SearchBookByAuthorView

app_name = BooksConfig.name

urlpatterns = [
    path('', BookListAPIView.as_view(), name='book_list'),
    path('search/', BookSearchView.as_view(), name='book_search'),
    path('create/', BookCreateAPIView.as_view(), name='book_create'),
    path('search/author/', SearchBookByAuthorView.as_view(), name='book_search_by_author'),
    path('<int:pk>/', BookRetrieveAPIView.as_view(), name='book_detail'),
    path('<int:pk>/update/', BookUpdateAPIView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteAPIView.as_view(), name='book_delete'),
]
