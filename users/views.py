from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer, UserSerializer, RegistrationSerializer
from .services import create_stripe_product, create_stripe_price, create_stripe_session

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user accounts.
    Provides create, retrieve, update, partial_update, and destroy functionality for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAuthenticated,]
        return super().get_permissions()

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payments.
    Provides create, retrieve, update, partial_update, destroy, and list functionality for payments.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class RegistrationAPIView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows new users to create an account.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

class PaymentCreateAPIView(generics.CreateAPIView):
    """
    API view for creating a payment and getting a Stripe checkout session.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        course = payment.paid_course

        stripe_product = create_stripe_product(course.title)
        stripe_price = create_stripe_price(stripe_product.id, payment.amount)
        stripe_session = create_stripe_session(stripe_price.id)

        payment.stripe_session_id = stripe_session.id
        payment.payment_link = stripe_session.url
        payment.save()
