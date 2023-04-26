from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.files.images import get_image_dimensions
from rest_framework import serializers
from .models import User, UserAgent, CustomeAuthToken
import re


class UserAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAgent
        fields = ('family', 'brand', 'model')


class CustomeAuthTokenSerializer(serializers.ModelSerializer):
    user_agent = UserAgentSerializer(many=False)

    class Meta:
        model = CustomeAuthToken
        fields =  ('token_key', 'user_agent')
    # def validate(self, data):
    #     print(data.get('id'))
    #     user_agent = UserAgent.objects.filter(id=data['id'])
    #     return user_agent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number')
        

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','email', 'password', 'password2', 'first_name', 'last_name', 'phone_number', 'image')

    def create(self, validated_data):
        validated_data.pop('password2')
        # print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user
        
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        phone_number = data.get('phone_number')
        if not password or not password == password2: 
            error = 'passwords do not match!'
            raise serializers.ValidationError(error)

        if not re.search("^09[0-9]{9}$", str(phone_number)):
            error = 'Phone is invalid!'
            raise serializers.ValidationError(error)
        return data
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')


class ChangePassSerializer(serializers.Serializer):
    old_pass = serializers.CharField(write_only=True)
    new_pass = serializers.CharField(write_only=True)  
    new_pass_repeat = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        if 'new_pass' in validated_data:
            instance.password = make_password(validated_data.get(
                'new_pass', instance.password
            ))
        instance.save()
        return instance
    
    def validate(self, data):
        old_pass = data.get('old_pass')
        new_pass = data.get('new_pass')
        new_pass_repeat = data.get('new_pass_repeat')
        # user = self.instance
        if not new_pass or not new_pass == new_pass_repeat:
            error = "Invalid inputs!"
            raise serializers.ValidationError(error)
        if old_pass == new_pass:
            error = "Password doesn't change!"
            raise serializers.ValidationError(error)
        return data


class SetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'image')
    
    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        phone_number = validated_data.get('phone_number')
        image = validated_data.get('image')
        instance.first_name = first_name if first_name else instance.first_name
        instance.last_name = last_name if last_name else instance.last_name
        instance.phone_number = phone_number if phone_number else instance.phone_number
        instance.image = image if image else instance.image
        instance.save()
        return instance

    def validate(self, data):
        phone_number = data.get('phone_number')
        image = data.get('image')
        if not re.search("^09[0-9]{9}$", str(phone_number)) and phone_number:
            error = 'Phone is invalid!'
            raise serializers.ValidationError(error)
        if image:
            w, h = get_image_dimensions(image)
            if w > 1000 or h > 1000:
                error = 'Image size should be less than or equal to 1000x1000 pixels'
                raise serializers.ValidationError(error)
            
        return data