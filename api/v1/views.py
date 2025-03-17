from django.db.models import Prefetch, Count, Q, Sum, F, ExpressionWrapper, FloatField
from django.db.models.expressions import RawSQL

from rest_framework import generics

from my_app.models import Lesson, Product, LessonUser
from my_app.serializers import LessonExtendedSerializer, ProductLessonSerializer, ProductStatsSerializer


class ListProductsLessons(generics.ListAPIView):
    """Lists all products with the associated lessons of each product which the user has access"""
    model = Product
    serializer_class = ProductLessonSerializer

    def get_queryset(self):
        user = self.request.user

        # Get products the  user has access to
        products = Product.objects.filter(access=user.id) \
            .prefetch_related(
                Prefetch(
                    'lesson__lessonuser_set',
                    queryset=LessonUser.objects.filter(user=user),
                    to_attr='user_data'
                )
            ) \
            .select_related('owner') \
            .only('id', 'name', 'owner__username')

        return products

class ListLessonsForProduct(generics.ListAPIView):
    """Lists the lessons for the given product"""
    model = Lesson
    serializer_class = LessonExtendedSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        user = self.request.user

        # Get lessons for the given product
        lessons = Lesson.objects.filter(products__access=user.id, products=product_id) \
            .prefetch_related(
                Prefetch(
                    'lessonuser_set',
                    queryset=LessonUser.objects.filter(user=user),
                    to_attr='user_data'
                )
            ).only('id', 'title', 'video', 'runtime')

        return lessons

class ListProductStats(generics.ListAPIView):
    model = Product
    serializer_class = ProductStatsSerializer

    def get_queryset(self):

        products = (Product.objects.annotate(
            total_views=Count(
                'lesson',
                filter=Q(lesson__lessonuser__status=LessonUser.LessonViewChoices.VIEWED)
            ),
            total_views_time=Sum(
                'lesson__lessonuser__viewed_time',
                filter=Q(lesson__lessonuser__status=LessonUser.LessonViewChoices.VIEWED)
            ),
            total_students=Count(
                'productaccess__user'
            ),
            acquisition_percentage=ExpressionWrapper(
                F('total_students') * 1.0 / RawSQL('(SELECT COUNT(*) FROM auth_user)', []),
                output_field=FloatField()
            )
        ).only('id', 'name'))

        return products

