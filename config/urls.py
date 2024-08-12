from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('authors/', include('authors.urls', namespace='authors')),
    path('books/', include('books.urls', namespace='books')),
    path('lendings/', include('lendings.urls', namespace='lendings')),
]
