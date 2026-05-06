from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.conf import settings
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({
                "access": access,
                "refresh": str(refresh),
                "role": user.role
            }, status=status.HTTP_201_CREATED)
        return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"errors": "Wrong Credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "access": access,
            "refresh": str(refresh),
            "role": user.role
        }, status=status.HTTP_200_OK)
