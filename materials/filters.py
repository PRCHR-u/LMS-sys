import django_filters
from django.db.models import Q, Count
from django.db import models
from .models import Course, Lesson


class CourseFilter(django_filters.FilterSet):
    """
    Фильтр для модели Course
    """
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название курса')
    description = django_filters.CharFilter(lookup_expr='icontains', label='Описание')
    owner = django_filters.NumberFilter(label='ID владельца')
    owner_email = django_filters.CharFilter(field_name='owner__email', lookup_expr='icontains', label='Email владельца')
    created_after = django_filters.DateFilter(field_name='id', lookup_expr='gte', label='Создан после')
    created_before = django_filters.DateFilter(field_name='id', lookup_expr='lte', label='Создан до')
    
    # Дополнительные фильтры
    has_lessons = django_filters.BooleanFilter(method='filter_has_lessons', label='С уроками')
    lesson_count_min = django_filters.NumberFilter(method='filter_lesson_count_min', label='Минимум уроков')
    lesson_count_max = django_filters.NumberFilter(method='filter_lesson_count_max', label='Максимум уроков')
    search = django_filters.CharFilter(method='filter_search', label='Поиск')
    
    def filter_has_lessons(self, queryset, name, value):
        """Фильтр курсов с уроками или без"""
        if value:
            return queryset.filter(lessons__isnull=False).distinct()
        return queryset.filter(lessons__isnull=True)
    
    def filter_lesson_count_min(self, queryset, name, value):
        """Фильтр по минимальному количеству уроков"""
        return queryset.annotate(
            lesson_count=Count('lessons')
        ).filter(lesson_count__gte=value)
    
    def filter_lesson_count_max(self, queryset, name, value):
        """Фильтр по максимальному количеству уроков"""
        return queryset.annotate(
            lesson_count=Count('lessons')
        ).filter(lesson_count__lte=value)
    
    def filter_search(self, queryset, name, value):
        """Поиск по названию и описанию"""
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
    
    class Meta:
        model = Course
        fields = {
            'title': ['exact', 'icontains', 'startswith'],
            'description': ['icontains'],
            'owner': ['exact'],
        }


class LessonFilter(django_filters.FilterSet):
    """
    Фильтр для модели Lesson
    """
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название урока')
    description = django_filters.CharFilter(lookup_expr='icontains', label='Описание')
    course = django_filters.NumberFilter(label='ID курса')
    course_title = django_filters.CharFilter(field_name='course__title', lookup_expr='icontains', label='Название курса')
    owner = django_filters.NumberFilter(label='ID владельца')
    owner_email = django_filters.CharFilter(field_name='owner__email', lookup_expr='icontains', label='Email владельца')
    has_video = django_filters.BooleanFilter(field_name='video_url', lookup_expr='isnull', exclude=True, label='С видео')
    
    # Дополнительные фильтры
    has_preview = django_filters.BooleanFilter(field_name='preview', lookup_expr='isnull', exclude=True, label='С превью')
    course_owner = django_filters.NumberFilter(field_name='course__owner', label='ID владельца курса')
    course_owner_email = django_filters.CharFilter(field_name='course__owner__email', lookup_expr='icontains', label='Email владельца курса')
    search = django_filters.CharFilter(method='filter_search', label='Поиск')
    
    def filter_search(self, queryset, name, value):
        """Поиск по названию, описанию и названию курса"""
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(description__icontains=value) | 
            Q(course__title__icontains=value)
        )
    
    class Meta:
        model = Lesson
        fields = {
            'title': ['exact', 'icontains', 'startswith'],
            'description': ['icontains'],
            'course': ['exact'],
            'owner': ['exact'],
            'video_url': ['isnull'],
        }
        filter_overrides = {
            models.ImageField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'lookup_expr': 'isnull',
                    'exclude': True,
                }
            }
        }
