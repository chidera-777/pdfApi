from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
                
class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
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
        
        