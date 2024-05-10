from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import resolve, reverse

from .models import Book, Review
from .views import BookListView, BookDetailView


class BookTests(TestCase):
    title = 'Foo1'
    author = 'John Don'
    price = 25.00
    user_email = 'tester@domain.com'
    user_password = 'testing123456'

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='tester',
            email=cls.user_email,
            password=cls.user_password
        )

        cls.verified_user = Permission.objects.get(codename="verified_user")

        cls.book = Book.objects.create(
            title=cls.title,
            author=cls.author,
            price=cls.price)

        cls.review = Review.objects.create(
            book=cls.book,
            author=cls.user,
            review='Great product test review'
        )

    def test_book_data(self):
        self.assertEqual(f"{self.book.title}", self.title)
        self.assertEqual(f"{self.book.author}", self.author)
        self.assertEqual(self.book.price, self.price)

    def test_book_listview(self):
        login = self.client.login(email=self.user_email, password=self.user_password)
        self.assertTrue(login)

        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_list.html')
        self.assertContains(response, 'Foo1')

        view = resolve('/books/')
        self.assertEqual(view.func.__name__, BookListView.as_view().__name__)

    def test_book_detailview_user_has_perm(self):
        login = self.client.login(email=self.user_email, password=self.user_password)
        self.assertTrue(login)
        self.user.user_permissions.add(self.verified_user)

        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'book_detail.html')
        self.assertContains(response, 'Foo1')
        self.assertContains(response, 'Great product test review')

        view = resolve(self.book.get_absolute_url())
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)

    def test_book_listview_user_not_logged(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'books_list.html')

    def test_book_detailview_user_not_logged(self):
        response = self.client.get(self.book.get_absolute_url())
        self.assertRedirects(response,
                             "{}?next={}".format(reverse("account_login"), self.book.get_absolute_url()))
        response = self.client.get("%s?next=/books/" % (reverse("account_login")))
        self.assertContains(response, "Log In")

    def test_book_add_review_user_has_perm(self):
        login = self.client.login(email=self.user_email, password=self.user_password)
        self.assertTrue(login)
        self.user.user_permissions.add(self.verified_user)

        post_request = self.client.post(self.book.get_absolute_url(),
                                        data={"book": self.book, "author": self.user, "review": "Another review!!!"})
        self.assertRedirects(post_request, self.book.get_absolute_url(), 302)

        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')
        self.assertContains(response, 'Foo1')
        self.assertContains(response, 'Another review!!!')

    def test_book_add_review_user_not_logged(self):
        login = self.client.login(email='wrongEmail@gmail.com', password=self.user_password)
        self.assertFalse(login)

        post_request = self.client.post(self.book.get_absolute_url(), data={"book": self.book,
                                                                            "author": self.user,
                                                                            "review": "This will not be added"})
        self.assertEqual(post_request.status_code, 302)

        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={self.book.get_absolute_url()}', 302)
