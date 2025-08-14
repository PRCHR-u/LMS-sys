from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer # Assuming you have these
from users.permissions import IsModerator # Import the custom permission

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer # Replace with your CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator] # Restrict create/destroy for moderators
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated | permissions.AllowAny] # Allow authenticated or unauthenticated for list/retrieve
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated, IsModerator] # Allow update/partial_update for moderators
        else:
            self.permission_classes = [permissions.IsAuthenticated] # Default for other actions

        return [permission() for permission in self.permission_classes]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer # Replace with your LessonSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator] # Restrict create/destroy for moderators
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated | permissions.AllowAny] # Allow authenticated or unauthenticated for list/retrieve
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated, IsModerator] # Allow update/partial_update for moderators
        else:
            self.permission_classes = [permissions.IsAuthenticated] # Default for other actions

        return [permission() for permission in self.permission_classes]
