from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_products')
    access = models.ManyToManyField(User, through='ProductAccess')
    lesson = models.ManyToManyField('Lesson', through='ProductLesson', related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductLesson(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lesson}-{self.product}"

class ProductAccess(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey('Permission', on_delete=models.SET_NULL, null=True)


class Permission(models.Model):

    name = models.CharField(max_length=100)
    view = models.BooleanField()
    edit = models.BooleanField()
    delete = models.BooleanField()

    def __str__(self):
        return f"{self.view}-{self.edit}-{self.delete}"

    @property
    def can_view(self):
        return self.view

    @property
    def can_edit(self):
        return self.edit

    @property
    def can_delete(self):
        return self.delete

class Lesson(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.URLField()
    runtime = models.IntegerField()
    user = models.ManyToManyField(User, through='LessonUser')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class LessonUser(models.Model):

    class LessonViewChoices(models.TextChoices):
        VIEWED = 'viewed'
        NOT_VIEWED = 'not_viewed'

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_time = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=LessonViewChoices, default=LessonViewChoices.NOT_VIEWED)
    last_viewed = models.DateTimeField(auto_now=True)
