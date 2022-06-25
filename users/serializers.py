from rest_framework import serializers
from rest_framework import viewsets
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from .models import AppUser

#User superclass serializer
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField()
    is_superuser = serializers.BooleanField(default=False)
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    #overrides default update
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            #hash the password field
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


#main AppUser serializer - User object is nested
class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    prof_type = serializers.ChoiceField(choices=AppUser.TeachingType, default=AppUser.TeachingType.TEACHING_PROF)
    is_peng = serializers.BooleanField(default=False)
    is_form_submitted = serializers.BooleanField(default=False)

    class Meta: 
        model = AppUser 
        fields = ('user', 'prof_type', 'is_peng', 'is_form_submitted')

    #overrides default create
    def create(self, validated_data):
        """
        Create and return a new AppUser instance, given the validated data.
        """
        user_data = validated_data.pop('user')

        #.create_user() automatically hashes the password field
        try:
            user = User.objects.create_user(**user_data)
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
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.update(instance.user, user_data)
        #then update AppUser
        super(AppUserSerializer, self).update(instance, validated_data)
        return instance
