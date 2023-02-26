from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

from .models import PDFModel

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
                
class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")
    password = serializers.CharField(style={'input_type':'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Passwords don\'t match')
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class UpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")
    
    class Meta:
        model = User
        fields = ['email', 'name', 'image']
        
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "A User with this email already exists"})
        return value
    
   
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(style={'input_type':'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don\'t match"})
        return attrs
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'})
    
    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")
        
        if not email and not password:
            raise serializers.ValidationError("Email and Password are required!!")
        
        if not User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email does not exist!!")
        
        request = self.context.get("request")
        user = authenticate(request, email=email, password=password)
        
        if not user:
            raise serializers.ValidationError("Wrong Crendentials!!")
        attrs['user'] = user
        return attrs
    

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.CharField()
    
    
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don\'t match"})
        return attrs

class PDFSerializer(serializers.ModelSerializer):
    category_data = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PDFModel
        fields = [
            'category_data',
            'title',
            'image',
            'download',
            'size',
            'created'
        ]
    
    def get_category_data(self, obj):
        return {
            "category": obj.category.category,
            "level": obj.category.level,
            "semester": obj.category.semester      
        }
        
        