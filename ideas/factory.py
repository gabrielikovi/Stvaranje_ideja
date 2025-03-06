import factory
from django.contrib.auth.models import User
from ideas.models import Profile, Idea, Comment
from faker import Faker

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    bio = factory.LazyAttribute(lambda _: fake.text())
    is_admin = factory.Faker('boolean')

class IdeaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Idea

    author = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=4))
    description = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=3))
    created_at = factory.LazyFunction(fake.date_time)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    idea = factory.SubFactory(IdeaFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=2))
    created_at = factory.LazyFunction(fake.date_time)
