from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_products')
    access = models.ManyToManyField(User, through='ProductAccess')
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, related_name='products')

    def __str__(self):
        return self.name

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
    status = models.ManyToManyField(User, through='LessonUser')

    def __str__(self):
        return self.title

class LessonUser(models.Model):

    class LessonViewChoices:
        VIEWED = 'viewed'
        NOT_VIEWED = 'not_viewed'

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_time = models.IntegerField()
    status = models.CharField(max_length=10, choices=LessonViewChoices, default=LessonViewChoices.NOT_VIEWED)
