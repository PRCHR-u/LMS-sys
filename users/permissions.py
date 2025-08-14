from rest_framework.permissions import BasePermission, IsAuthenticated


class IsModerator(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.groups.filter(name='Moderators').exists()
