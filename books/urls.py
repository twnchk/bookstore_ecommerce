from django.urls import path
from .views import BookListView, BookView, SearchResultsListView

urlpatterns = [
    path('', BookListView.as_view(), name='books_list'),
    path('<uuid:pk>/', BookView.as_view(), name='book_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
]
