from django.urls import path
from materials.views import (CourseViewSet, LessonViewSet, SubscriptionAPIView)
from rest_framework.routers import DefaultRouter

app_name = 'materials'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
]

urlpatterns += router.urls
