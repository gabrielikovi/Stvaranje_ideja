from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ideas.models import Idea

class UrlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.idea = Idea.objects.create(author=self.user, title="Test Idea", description="Test description")

    def test_public_urls(self):
        urls = [
            reverse("login"),
            reverse("register"),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Fail on {url}")

    def test_protected_urls_redirect_for_anonymous_users(self):
        urls = [
            reverse("idea_list"),
            reverse("idea_create"),
            reverse("idea_detail", args=[self.idea.id]),
            reverse("idea_update", args=[self.idea.id]),
            reverse("idea_delete", args=[self.idea.id]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f"Fail on {url}")

    def test_protected_urls_work_for_authenticated_users(self):
        self.client.login(username="testuser", password="password123")
        urls = [
            reverse("idea_list"),
            reverse("idea_create"),
            reverse("idea_detail", args=[self.idea.id]),
            reverse("idea_update", args=[self.idea.id]),
            reverse("idea_delete", args=[self.idea.id]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Fail on {url}")
