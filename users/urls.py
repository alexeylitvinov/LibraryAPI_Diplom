from django.urls import path
from rest_framework.permissions import AllowAny

from .apps import UsersConfig
from .views import UserListAPIView, UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserPasswordUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny, )), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('users/', UserListAPIView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='users_detail'),
    # path('library_card/<str:library_card>/', GetUserByDocumentView.as_view(), name='users_by_document'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='users_update'),
    path('users/<int:pk>/update/password/', UserPasswordUpdateAPIView.as_view(), name='users_update_password'),
]
