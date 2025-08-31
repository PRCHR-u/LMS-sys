"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys
import os

# Get the project root directory (assuming manage.py is in the parent directory of mysite)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.insert(0, project_root)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
from users.views import PaymentViewSet, RegistrationAPIView, UserViewSet

# Создаем роутер для пользователей
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),
    
    # API маршруты
    path('api/', include([
        # Маршруты для материалов (курсы и уроки)
        path('materials/', include('materials.urls')),
        
        # Маршруты для пользователей и платежей
        path('', include(router.urls)),
        
        # Дополнительные маршруты для пользователей
        path('users/', include('users.urls')),
        
        # Аутентификация JWT
        path('auth/', include([
            path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('register/', RegistrationAPIView.as_view(), name='register'),
        ])),
    ])),
    
    # Корневой маршрут для API
    path('', include(router.urls)),
]
