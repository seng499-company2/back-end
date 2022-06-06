from rest_framework import serializers
from rest_framework import viewsets

from django.contrib.auth.models import User
from .models import AppUser

class AppUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    prof_type = serializers.ChoiceField(choices=AppUser.TeachingType, default=AppUser.TeachingType.TEACHING_PROF)
    class Meta: 
        model = AppUser 
        fields = ('user_id', 'prof_type', 'username', 'password', 'first_name', 'last_name' 'email', 'is_superuser')

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

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=is_superuser
            )
        appUser = AppUser.objects.create(user=user, **validated_data)
        return appUser

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
        '''instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance'''