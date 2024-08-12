from django.urls import path

from lendings.apps import LendingsConfig
from lendings.views import LendingCreateAPIView, LendingListAPIView, LendingRetrieveAPIView, LendingActionAPIView

app_name = LendingsConfig.name

urlpatterns = [
    path('', LendingListAPIView.as_view(), name='lending_list'),
    path('create/', LendingCreateAPIView.as_view(), name='lending_create'),
    path('<int:pk>/', LendingRetrieveAPIView.as_view(), name='lending_detail'),
    path('<int:pk>/return/', LendingActionAPIView.as_view(), name='lending_return'),
]
