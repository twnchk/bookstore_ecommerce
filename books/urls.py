from django.urls import path
from .views import BookListView, BookView

urlpatterns = [
    path('', BookListView.as_view(), name='books_list'),
    path('<uuid:pk>/', BookView.as_view(), name='book_detail'),
]
