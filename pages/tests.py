from django.test import SimpleTestCase
from django.urls import reverse, resolve

from pages.views import HomePageView, AboutPageView


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template_used(self):
        self.assertTemplateUsed(self.response, 'home.html')
        self.assertContains(self.response, "Homepage")

    def test_homepage_template_used_does_not_contain_message(self):
        self.assertTemplateUsed(self.response, 'home.html')
        self.assertNotContains(self.response, "Some random message")

    def test_homepage_view_location(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)

    def test_aboutpage(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'about.html')
        self.assertContains(self.response, 'About page')

    def test_aboutpage_view(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)
