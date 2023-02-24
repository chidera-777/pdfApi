from django.contrib.auth import get_user_model, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView

from .serializers import RegisterSerializer, UserSerializer, UpdateSerializer, LoginSerializer, PDFSerializer, ChangePasswordSerializer
from .models import PDFModel


User = get_user_model()
# Create your views here.
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "success": "User created Successfully!!!",
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)
        
register_apiView = RegisterAPIView.as_view()


class UpdateAPIResponseView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
update_view = UpdateAPIResponseView.as_view()


class ChangePasswordAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_field = 'pk'
    
    def update(self, request):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            password = serializer.data.get('password')        
            if not user.check_password(old_password):
                return Response({
                    "old_password": "Old password is not correct!!"
                })
            user.set_password(password)
            user.save()
            return Response({
                "success": "Password have been updated Successfully!!",
                'status': status.HTTP_200_OK
            })
        return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)
        
    
update_password = ChangePasswordAPIView.as_view()

        
class LoginAPIView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)
    
class PDFAPIView(generics.ListAPIView):
    queryset = PDFModel.objects.all()
    serializer_class = PDFSerializer
    
pdf_list = PDFAPIView.as_view()
           
