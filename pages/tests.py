from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_view_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template_used(self):
        self.assertTemplateUsed(self.response, 'home.html')
        self.assertContains(self.response, "Homepage")

    def test_homepage_template_used_does_not_contain_message(self):
        self.assertTemplateUsed(self.response, 'home.html')
        self.assertNotContains(self.response, "Some random message")
