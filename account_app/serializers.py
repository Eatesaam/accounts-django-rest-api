from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['is_verified']

    def create(self, validated_data):

        password = validated_data['password']
        confirm_password = validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError(
                {'error': 'password and confirm_password must be the same!'})

        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists!'})

        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError(
                {'error': 'Username already exists!'})

        user = User(
            email=validated_data['email'], username=validated_data['username'], password=make_password(validated_data['password']))

        user.save()

        return user
