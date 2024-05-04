from django.test import TestCase
from django.urls import resolve

from .models import Book
from .views import BookListView, BookDetailView


class BookTests(TestCase):
    title = 'Foo1'
    author = 'John Don'
    price = 25.00

    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(title=cls.title, author=cls.author, price=cls.price)

    def test_book_data(self):
        self.assertEqual(f"{self.book.title}", self.title)
        self.assertEqual(f"{self.book.author}", self.author)
        self.assertEqual(self.book.price, self.price)

    def test_book_listview(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_list.html')
        self.assertContains(response, 'Foo1')

        view = resolve('/books/')
        self.assertEqual(view.func.__name__, BookListView.as_view().__name__)

    def test_book_detailview(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'book_detail.html')
        self.assertContains(response, 'Foo1')

        view = resolve(self.book.get_absolute_url())
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)
