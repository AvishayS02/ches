from rest_framework import serializers
from django.contrib.auth import get_user_model , authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # We use `get()` to avoid KeyErrors if `email` is missing
        email = validated_data.get('email', None)  # email can be None
        username = validated_data['username']
        password = validated_data['password']
        
        # Create the user instance
        user = User(username=username, email=email)
        
        # Set the hashed password
        user.set_password(password)
        
        # Save the user instance to the database
        user.save()
        
        return user
    
def validate(self, attrs):
        # Check that passwords match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        return attrs
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

