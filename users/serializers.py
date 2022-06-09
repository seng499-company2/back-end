from rest_framework import serializers
from rest_framework import viewsets
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from .models import AppUser

#User superclass serializer
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField()
    is_superuser = serializers.BooleanField(default=False)
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_superuser')


#main AppUser serializer - User object is nested
class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    prof_type = serializers.ChoiceField(choices=AppUser.TeachingType, default=AppUser.TeachingType.TEACHING_PROF)
    class Meta: 
        model = AppUser 
        fields = ('user', 'prof_type')

    #overrides default create
    def create(self, validated_data):
        """
        Create and return a new AppUser instance, given the validated data.
        """
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        is_superuser = validated_data.pop('is_superuser')

        #.create_user() automatically hashes the password field
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_superuser=is_superuser
                )
            appUser = AppUser.objects.create(user=user, **validated_data)
        
        #raising a JSON-like exception
        except ValidationError:
            raise serializers.ValidationError({"error": "Invalid input!"})
        return appUser

    #overrides default update
    def update(self, instance, validated_data):
        """
        Update and return an existing AppUser instance, given the validated data.
        """
        #update the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        #then update AppUser
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance