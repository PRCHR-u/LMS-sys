from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для курсов с полными CRUD-операциями
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Автоматически устанавливает владельца курса"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Получить все уроки для конкретного курса"""
        course = self.get_object()
        lessons = course.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Записаться на курс"""
        course = self.get_object()
        # Здесь можно добавить логику записи на курс
        return Response({'message': f'Вы записались на курс "{course.title}"'}, 
                       status=status.HTTP_200_OK)


class CourseListView(generics.ListAPIView):
    """Список всех курсов (только чтение)"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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
    serializer_class = CourseSerializer
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
