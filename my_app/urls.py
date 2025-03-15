from django.urls import path
from my_app.views import index

urlpatterns =  [
    path('', index, name='index'),
]