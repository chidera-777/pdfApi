from django.contrib.auth import get_user_model, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags

from .serializers import RegisterSerializer, UserSerializer, UpdateSerializer, LoginSerializer, PDFSerializer, ChangePasswordSerializer, ResetPasswordEmailSerializer, ResetPasswordSerializer
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


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            old_password = serializer.validated_data['old_password']
            password = serializer.validated_data['password']                
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
        
        
class LoginAPIView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)
    

class ResetPasswordEmailView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                 return Response({
                    'error': 'A User with this email does not exist!!',
                    'status': status.HTTP_404_NOT_FOUND
                })
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
               
                subject = 'Reset password for User at ECE Departmental Website'
                context = {
                    'domain': f'http://localhost:3000/password-reset/{uid}/{token}',
                    'email': user.email,
                    'token': token,
                    'uid': uid
                    }
                message = render_to_string('password_reset_email.html', context)
                content = strip_tags(message)
                from_email = 'ferdinandchidera49@gmail.com'
                to_email = [user.email]
                send_mail(subject, content, from_email, to_email, fail_silently=False)
                
                return Response({
                    "success": "An email has been sent to reset your password",
                    'status': status.HTTP_200_OK
                })
            return Response({
                'error': 'Invalid Details!!',
                'status': status.HTTP_404_NOT_FOUND
            })                  


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if serializer.is_valid(raise_exception=True):
            if user and default_token_generator.check_token(user, token):
                new_password = serializer.validated_data['password']
                user.set_password(new_password)
                user.save()
                return Response({
                    "success": "Password have been updated Successfully!!",
                    'status': status.HTTP_200_OK
                })
            return Response({
                    'error': "Invalid Token",
                    'status': status.HTTP_404_NOT_FOUND
                })          
        
    
class PDFAPIView(generics.ListAPIView):
    queryset = PDFModel.objects.all()
    serializer_class = PDFSerializer
    


register_apiView = RegisterAPIView.as_view()
update_view = UpdateAPIResponseView.as_view()
update_password = ChangePasswordAPIView.as_view()
reset_password = ResetPasswordEmailView.as_view() 
reset_password_confirm = ResetPasswordView.as_view()        
pdf_list = PDFAPIView.as_view()
           
