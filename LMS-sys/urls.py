from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import PaymentViewSet, RegistrationAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Роутер для пользователей
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include(router.urls)),
        path('materials/', include('materials.urls')),
        path('users/', include('users.urls')),
        
        path('auth/register/', RegistrationAPIView.as_view(), name='register'),
        path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
