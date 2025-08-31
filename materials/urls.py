from django.urls import path
from materials.views import (LessonListAPIView, LessonRetrieveAPIView,
                             LessonCreateAPIView, LessonUpdateAPIView,
                             LessonDestroyAPIView, CourseViewSet, CourseListView,
                             CourseCreateAPIView, CourseRetrieveAPIView,
                             CourseUpdateAPIView, CourseDestroyAPIView)
from rest_framework.routers import DefaultRouter

# Создаем роутер для ViewSet курсов
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    # Маршруты для курсов (через ViewSet - автоматически создает все CRUD операции)
    # GET /materials/courses/ - список всех курсов
    # POST /materials/courses/ - создание нового курса
    # GET /materials/courses/{id}/ - получение курса по ID
    # PUT /materials/courses/{id}/ - полное обновление курса
    # PATCH /materials/courses/{id}/ - частичное обновление курса
    # DELETE /materials/courses/{id}/ - удаление курса
    # GET /materials/courses/{id}/lessons/ - получение уроков курса
    # POST /materials/courses/{id}/enroll/ - запись на курс
    
    # Альтернативные маршруты для курсов (через Generic Views)
    path('courses/list/', CourseListView.as_view(), name='course-list'),  # GET - список курсов
    path('courses/create/', CourseCreateAPIView.as_view(), name='course-create'),  # POST - создание курса
    path('courses/<int:pk>/', CourseRetrieveAPIView.as_view(), name='course-detail'),  # GET - получение курса
    path('courses/<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course-update'),  # PUT/PATCH - обновление курса
    path('courses/<int:pk>/delete/', CourseDestroyAPIView.as_view(), name='course-delete'),  # DELETE - удаление курса
    
    # Маршруты для уроков (через Generic Views)
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),  # GET - список уроков
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),  # POST - создание урока
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),  # GET - получение урока
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),  # PUT/PATCH - обновление урока
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),  # DELETE - удаление урока
]

# Добавляем маршруты от роутера
urlpatterns += router.urls