from django.urls import path

from authors.apps import AuthorsConfig
from authors.views import AuthorCreateAPIView, AuthorListAPIView, AuthorRetrieveAPIView, AuthorUpdateAPIView, \
    AuthorDeleteAPIView, AuthorSearchView

app_name = AuthorsConfig.name

urlpatterns = [
    path('', AuthorListAPIView.as_view(), name='author_list'),
    path('create/', AuthorCreateAPIView.as_view(), name='author_create'),
    path('search/', AuthorSearchView.as_view(), name='author_search'),
    path('<int:pk>/', AuthorRetrieveAPIView.as_view(), name='author_detail'),
    path('<int:pk>/update/', AuthorUpdateAPIView.as_view(), name='author_update'),
    path('<int:pk>/delete/', AuthorDeleteAPIView.as_view(), name='author_delete'),

]
