from django.contrib.auth import get_user_model, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView

from .models import Profile
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer


User = get_user_model()
# Create your views here.
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Profile.objects.create(user=user)
        return Response({
            "success": "User created Successfully!!!",
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)
        
register_apiView = RegisterAPIView.as_view()
        
        
class LoginAPIView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)
           
