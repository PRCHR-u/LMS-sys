from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, CourseDetailSerializer, LessonSerializer, LessonInCourseSerializer, LessonCreateInCourseSerializer
from materials.filters import CourseFilter, LessonFilter

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для курсов с полными CRUD-операциями
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'id']
    ordering = ['title']
    
    def get_serializer_class(self):
        """Выбирает подходящий сериализатор в зависимости от действия"""
        if self.action == 'retrieve':
            return CourseDetailSerializer
        elif self.action == 'add_lesson':
            return LessonCreateInCourseSerializer
        return CourseSerializer
    
    def perform_create(self, serializer):
        """Автоматически устанавливает владельца курса"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Получить все уроки для конкретного курса"""
        course = self.get_object()
        lessons = course.lessons.all()
        serializer = LessonInCourseSerializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Записаться на курс"""
        course = self.get_object()
        # Здесь можно добавить логику записи на курс
        return Response({'message': f'Вы записались на курс "{course.title}"'}, 
                       status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_lesson(self, request, pk=None):
        """Добавить урок в курс"""
        course = self.get_object()
        serializer = LessonCreateInCourseSerializer(data=request.data)
        
        if serializer.is_valid():
            lesson = serializer.save(course=course, owner=request.user)
            lesson_serializer = LessonInCourseSerializer(lesson)
            return Response(lesson_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListView(generics.ListAPIView):
    """Список всех курсов (только чтение)"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'id']
    ordering = ['title']


class CourseCreateAPIView(generics.CreateAPIView):
    """Создание нового курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """Получение курса по ID"""
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CourseUpdateAPIView(generics.UpdateAPIView):
    """Обновление курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Пользователь может редактировать только свои курсы"""
        return Course.objects.filter(owner=self.request.user)


class CourseDestroyAPIView(generics.DestroyAPIView):
    """Удаление курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Пользователь может удалять только свои курсы"""
        return Course.objects.filter(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Список всех уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LessonFilter
    search_fields = ['title', 'description', 'course__title']
    ordering_fields = ['title', 'id', 'course__title']
    ordering = ['title']


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание нового урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Получение урока по ID"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Пользователь может редактировать только свои уроки"""
        return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Пользователь может удалять только свои уроки"""
        return Lesson.objects.filter(owner=self.request.user)
