import random
from django.db import transaction
from django.core.management.base import BaseCommand
from ideas.models import Profile, Idea, Comment
from ideas.factory import UserFactory, ProfileFactory, IdeaFactory, CommentFactory

NUM_USERS = 10
NUM_IDEAS = 30
NUM_COMMENTS = 50

class Command(BaseCommand):
    help = "Generira testne podatke"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Brišem stare podatke...")
        models = [Profile, Idea, Comment]
        for model in models:
            model.objects.all().delete()

        self.stdout.write("Kreiranje novih podataka...")

        users = UserFactory.create_batch(NUM_USERS)
        self.stdout.write(f"Kreirano {len(users)} korisnika.")

        profiles = [ProfileFactory(user=user) for user in users]
        self.stdout.write(f"Kreirano {len(profiles)} profila.")

        ideas = IdeaFactory.create_batch(NUM_IDEAS, author=random.choice(users))
        self.stdout.write(f"Kreirano {len(ideas)} ideja.")

        comments = [CommentFactory(idea=random.choice(ideas), author=random.choice(users)) for _ in range(NUM_COMMENTS)]
        self.stdout.write(f"Kreirano {len(comments)} komentara.")

        self.stdout.write(self.style.SUCCESS("Uspješno generirani testni podaci!"))
