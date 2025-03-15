from django.db.models import Count
from rest_framework import serializers
from my_app.models import Lesson, Product, LessonUser


class LessonSerializer(serializers.ModelSerializer):

    viewed_time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'viewed_time', 'status')

    def get_viewed_time(self, obj):
        if hasattr(obj, 'user_data') and obj.user_data:
            return obj.user_data[0].viewed_time

        return -1

    def get_status(self, obj):
        if hasattr(obj, 'user_data') and obj.user_data:
            return obj.user_data[0].status

        return LessonUser.LessonViewChoices.NOT_VIEWED

class LessonExtendedSerializer(serializers.ModelSerializer):

    viewed_time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    last_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'viewed_time', 'status', 'last_viewed')

    def get_viewed_time(self, obj):
        if hasattr(obj, 'user_data') and obj.user_data:
            return obj.user_data[0].viewed_time

        return -1

    def get_status(self, obj):
        if hasattr(obj, 'user_data') and obj.user_data:
            return obj.user_data[0].status

        return None

    def get_last_viewed(self, obj):
        if hasattr(obj, 'user_data') and obj.user_data:
            return obj.user_data[0].last_viewed

        return None

class ProductLessonSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True, source='lesson')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = ('id', 'name', 'owner', 'lessons')

class ProductStatsSerializer(serializers.ModelSerializer):

    total_views = serializers.IntegerField()
    total_views_time = serializers.IntegerField()
    total_students = serializers.IntegerField()
    acquisition_percentage = serializers.FloatField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'total_views', 'total_views_time', 'total_students', 'acquisition_percentage')
