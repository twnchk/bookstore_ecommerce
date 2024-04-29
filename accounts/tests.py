from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="testUser", email="test@test.com", password="testing123456")

        self.assertEqual(user.username, "testUser")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(username="superUser", email="superUser@test.com", password="testing123456")

        self.assertEqual(user.username, "superUser")
        self.assertEqual(user.email, "superUser@test.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
