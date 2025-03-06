from django.test import TestCase
from django.contrib.auth.models import User
from ideas.models import Profile, Idea, Comment

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

        self.profile = Profile.objects.create(user=self.user, bio="This is a test bio", is_admin=True)

        self.idea = Idea.objects.create(
            author=self.user,
            title="Test Idea",
            description="This is a test idea description"
        )

        self.comment = Comment.objects.create(
            idea=self.idea,
            author=self.user,
            content="This is a test comment"
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, "This is a test bio")
        self.assertTrue(self.profile.is_admin)

    def test_profile_str_representation(self):
        self.assertEqual(str(self.profile), self.user.username)

    def test_idea_creation(self):
        self.assertEqual(self.idea.author, self.user)
        self.assertEqual(self.idea.title, "Test Idea")
        self.assertEqual(self.idea.description, "This is a test idea description")

    def test_idea_str_representation(self):
        self.assertEqual(str(self.idea), "Test Idea")

    def test_comment_creation(self):
        self.assertEqual(self.comment.idea, self.idea)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, "This is a test comment")

    def test_comment_str_representation(self):
        expected_str = f"Komentar od {self.user.username} na {self.idea.title}"
        self.assertEqual(str(self.comment), expected_str)
