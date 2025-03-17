from django.contrib import admin
from my_app.models import *

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Permission)
admin.site.register(ProductLesson)
admin.site.register(ProductAccess)
admin.site.register(LessonUser)