from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from paginators import CustomPaginator
from .tasks import send_update_email

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for interacting with Course instances.
    Provides create, retrieve, update, partial_update, destroy, and list functionality for courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('title',)
    ordering_fields = ('update_date',)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Overrides the default update behavior to send email notifications to subscribers.
        """
        instance = serializer.save()
        subscriptions = Subscription.objects.filter(course=instance)
        for sub in subscriptions:
            if sub.user.email:
                send_update_email.delay(sub.user.email, instance.title)

    def get_queryset(self):
        if not self.request.user.groups.filter(name='Moderator').exists():
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.all()

class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for interacting with Lesson instances.
    Provides create, retrieve, update, partial_update, destroy, and list functionality for lessons.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPaginator
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('title', 'course',)
    ordering_fields = ('update_date',)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if not self.request.user.groups.filter(name='Moderator').exists():
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()

class SubscriptionAPIView(APIView):
    """
    API view for managing user subscriptions to courses.
    Allows users to subscribe to or unsubscribe from a course.
    """
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})
