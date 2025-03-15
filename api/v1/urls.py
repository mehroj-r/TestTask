from django.urls import path
from api.v1.views import ListProductsLessons, ListLessonsForProduct, ListProductStats

urlpatterns = [
    path('products/', ListProductsLessons.as_view()),
    path('products/<int:product_id>/lessons/', ListLessonsForProduct.as_view()),
    path('product-stats/', ListProductStats.as_view()),
]