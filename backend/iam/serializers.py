from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'nickname', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        user = User.objects.create_user(**validated_data)

        return user

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="Username or E-mail")
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        user = User.objects.filter(email=identifier).first() or User.objects.filter(email=identifier).first()

        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError({"password": "Your account has been disabled"})

            attrs['user'] = user
            return attrs

        raise serializers.ValidationError({"password": "Credentials not correct"})

class UserResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'nickname']

