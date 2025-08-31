from rest_framework import serializers
from materials.models import Course, Lesson
from django.conf import settings

class LessonSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор для урока со всеми полями
    """
    class Meta:
        model = Lesson
        fields = '__all__'


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

    def get_lesson_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор для курса с полной информацией об уроках
    """
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonInCourseSerializer(many=True, read_only=True)
    owner_email = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()

    def get_owner_email(self, obj):
        """Возвращает email владельца курса"""
        return obj.owner.email if obj.owner else None

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'owner', 'owner_email', 'lesson_count', 'lessons']