# populate_db.py
import random
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth.models import User
from my_app.models import Product, Permission, Lesson, ProductLesson, ProductAccess, LessonUser


def create_users(num_users=5):
    """Create test users"""
    users = []
    for i in range(num_users):
        username = f'user{i + 1}'
        email = f'user{i + 1}@example.com'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': f'First{i + 1}',
                'last_name': f'Last{i + 1}'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {username}")
        else:
            print(f"User {username} already exists")
        users.append(user)
    return users


def create_permissions():
    """Create different permission levels"""
    permissions = []

    # Read-only permission
    view_only, _ = Permission.objects.get_or_create(
        name='View Only',
        defaults={'view': True, 'edit': False, 'delete': False}
    )
    permissions.append(view_only)

    # Editor permission
    editor, _ = Permission.objects.get_or_create(
        name='Editor',
        defaults={'view': True, 'edit': True, 'delete': False}
    )
    permissions.append(editor)

    # Admin permission
    admin, _ = Permission.objects.get_or_create(
        name='Admin',
        defaults={'view': True, 'edit': True, 'delete': True}
    )
    permissions.append(admin)

    print(f"Created {len(permissions)} permission types")
    return permissions


def create_lessons(num_lessons=10):
    """Create test lessons"""
    lessons = []
    for i in range(num_lessons):
        title = f'Lesson {i + 1}'
        description = f'This is a detailed description for lesson {i + 1}.'
        video = f'https://example.com/videos/lesson{i + 1}.mp4'
        runtime = random.randint(300, 3600)  # Runtime between 5 minutes and 1 hour in seconds

        lesson, created = Lesson.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'video': video,
                'runtime': runtime
            }
        )
        if created:
            print(f"Created lesson: {title}")
        lessons.append(lesson)
    return lessons


def create_products(users, lessons, num_products=3):
    """Create test products and associate lessons with them"""
    products = []
    for i in range(num_products):
        owner = random.choice(users)
        name = f'Product {i + 1}'

        product, created = Product.objects.get_or_create(
            name=name,
            defaults={'owner': owner}
        )
        if created:
            print(f"Created product: {name}")

        # Associate random lessons with this product
        num_lessons_for_product = random.randint(3, len(lessons))
        selected_lessons = random.sample(lessons, num_lessons_for_product)

        for lesson in selected_lessons:
            ProductLesson.objects.get_or_create(
                product=product,
                lesson=lesson
            )
            print(f"Associated lesson '{lesson.title}' with product '{product.name}'")

        products.append(product)
    return products


def create_lesson_user_relationships(user, product):
    """Create LessonUser entries for all lessons in a product for a specific user"""
    # Get all lessons associated with the product
    product_lessons = ProductLesson.objects.filter(product=product)

    for product_lesson in product_lessons:
        lesson = product_lesson.lesson
        # Create LessonUser entry with default values
        lesson_user, created = LessonUser.objects.get_or_create(
            lesson=lesson,
            user=user,
            defaults={
                'viewed_time': 0,
                'status': LessonUser.LessonViewChoices.NOT_VIEWED
            }
        )
        if created:
            print(f"Created LessonUser relationship for {user.username} and lesson '{lesson.title}'")


def assign_product_access(users, products, permissions):
    """Assign product access to users with different permission levels"""
    for product in products:
        # Get the product owner
        owner = product.owner

        # Create LessonUser relationships for the owner
        create_lesson_user_relationships(owner, product)
        print(f"Created lesson relationships for owner {owner.username} of product '{product.name}'")

        # Available users (excluding the owner)
        available_users = [user for user in users if user != owner]

        # Randomly select users to have access (at least 1, at most all available users)
        num_users_with_access = random.randint(1, len(available_users))
        users_with_access = random.sample(available_users, num_users_with_access)

        for user in users_with_access:
            # Randomly assign a permission level
            permission = random.choice(permissions)

            # Create ProductAccess entry
            product_access, created = ProductAccess.objects.get_or_create(
                product=product,
                user=user,
                defaults={'permission': permission}
            )

            if created:
                print(f"Granted {permission.name} access to {user.username} for {product.name}")

            # Create LessonUser relationships for all lessons in the product
            create_lesson_user_relationships(user, product)


def run():
    """Main function to populate the database"""
    print("Starting database population script...")

    # Create test data
    users = create_users()
    permissions = create_permissions()
    lessons = create_lessons()
    products = create_products(users, lessons)

    # Assign product access and create necessary LessonUser relationships
    assign_product_access(users, products, permissions)

    print("Database population complete!")


if __name__ == "__main__":
    run()