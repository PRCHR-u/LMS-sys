from django.urls import path
from materials.views import (LessonListAPIView, LessonRetrieveAPIView,
                             LessonCreateAPIView, LessonUpdateAPIView,
                             LessonDestroyAPIView)

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
]
