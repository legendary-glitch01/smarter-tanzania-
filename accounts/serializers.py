from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()
class ProfileSerializer(serializers.ModelSerializer):
    # We pull the username and email from the related User model
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Profile
        fields = ['username', 'email', 'avatar', 'bio', 'birth_date', 'registration_method']
        # The registration method should generally stay fixed
        read_only_fields = ['registration_method']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user