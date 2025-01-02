from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer

# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)

    if serializer.is_valid():
        tokens = serializer.validated_data

        return Response(
            {
                "message": "Login success",
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "id": tokens.get("id"),
                "username": tokens.get("username"),
                "email": tokens.get("email"),
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_registration_view(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response({"error": "Refresh token required"}, status=400)

    try:
        token = RefreshToken(refresh_token) # Blacklisitng the token.

        token.blacklist()

        return Response({"message": "Successfully logged out"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
