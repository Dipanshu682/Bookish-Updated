from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.models import Book, Category
from faker import Faker
import random

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = 'Generate dummy users, categories, and books'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating dummy users...")
        users = self.create_dummy_users()

        self.stdout.write("Creating categories...")
        categories = self.create_dummy_categories()

        self.stdout.write("Creating dummy books...")
        self.create_dummy_books(users, categories)

        self.stdout.write(self.style.SUCCESS("✅ Dummy data created successfully."))

    def create_dummy_users(self, n=5):
        users = []
        for i in range(n):
            username = f"user{i}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com"
                }
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)
        return users

    def create_dummy_categories(self):
        category_names = ['Fiction', 'Science', 'Math', 'History', 'Comics']
        category_objs = []
        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name)
            category_objs.append(category)
        return category_objs

    def create_dummy_books(self, users, categories, n=20):
        for _ in range(n):
            Book.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                price=random.randint(100, 500),
                category=random.choice(categories),
                seller=random.choice(users),
                condition=random.choice(['New', 'Good', 'Used']),
                status=random.choice(['Available', 'Sold']),
                quantity=random.randint(1, 5)
            )
