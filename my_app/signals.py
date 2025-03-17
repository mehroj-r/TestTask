from pprint import pprint

from django.db import connection
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from my_app.models import LessonUser


@receiver(pre_save, sender=LessonUser)
def updateViewStatus(sender, instance, **kwargs):
    """Update the view status of the lesson after watching >=80%"""

    if instance.status == LessonUser.LessonViewChoices.NOT_VIEWED and instance.viewed_time/instance.lesson.runtime >= 0.8:
        instance.status = LessonUser.LessonViewChoices.VIEWED

    pprint(connection.queries)