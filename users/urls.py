from django.urls import path
from users.views import ProfileUpdateAPIView

urlpatterns = [
    # Эндпоинт для редактирования профиля
    path('profile/', ProfileUpdateAPIView.as_view(), name='profile-update'),
]
