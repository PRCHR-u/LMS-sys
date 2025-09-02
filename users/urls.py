from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentCreateAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
]
