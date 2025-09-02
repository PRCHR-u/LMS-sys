from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from django.conf import settings
from .validators import YoutubeURLValidator

class LessonSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор для урока со всеми полями
    """
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YoutubeURLValidator(field='video_url')]


class LessonInCourseSerializer(serializers.ModelSerializer):
    """
    Упрощенный сериализатор для урока, используемый в курсе
    Исключает поле course для избежания циклических зависимостей
    """
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'owner']


class LessonCreateInCourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания урока в курсе
    Автоматически устанавливает курс из URL параметра
    """
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для курса с количеством уроков и списком уроков
    """
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonInCourseSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Возвращает статус подписки текущего пользователя на курс"""
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'owner', 'lesson_count', 'lessons', 'is_subscribed']


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор для курса с полной информацией об уроках
    """
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonInCourseSerializer(many=True, read_only=True)
    owner_email = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()

    def get_owner_email(self, obj):
        """Возвращает email владельца курса"""
        return obj.owner.email if obj.owner else None

    def get_is_subscribed(self, obj):
        """Возвращает статус подписки текущего пользователя на курс"""
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'owner', 'owner_email', 'lesson_count', 'lessons', 'is_subscribed']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
