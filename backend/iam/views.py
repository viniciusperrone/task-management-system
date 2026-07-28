from django.contrib.auth.models import update_last_login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from iam.filters import UserFilter
from iam.models import User
from iam.serializers import RegisterSerializer, LoginSerializer, UserProfileUpdateSerializer, UserResponseSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "user": UserResponseSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            update_last_login(None, user)

            refresh = RefreshToken.for_user(user)

            return Response({
                "user": UserResponseSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = UserResponseSerializer
    queryset = User.objects.all().order_by("first_name", "username")

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'first_name', 'last_name', 'nickname']
    ordering_fields = ['username', 'email', 'created_at']
