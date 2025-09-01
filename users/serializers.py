from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Payment

User = get_user_model()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone', 'city', 'avatar')

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля пользователя
    """
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'city', 'avatar')
        read_only_fields = ('id', 'date_joined', 'last_login')
    
    def validate_email(self, value):
        """
        Проверяем, что email уникален (если изменяется)
        """
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value
    
    def validate_username(self, value):
        """
        Проверяем, что username уникален (если изменяется)
        """
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким username уже существует.")
        return value
    
    def update(self, instance, validated_data):
        """
        Обновляем профиль пользователя
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'username')

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data.get('username') or email
        
        if User.objects.filter(username=username).exists():
             import uuid
             username = f"{username}_{uuid.uuid4().hex[:4]}"

        user = User.objects.create_user(
            email=email,
            username=username,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user
