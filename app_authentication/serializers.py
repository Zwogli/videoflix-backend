from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_name', 'password']    #'first_name', 'last_name',
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_name=validated_data.get('user_name', ''),
            # first_name=validated_data.get('first_name', ''),
            # last_name=validated_data.get('last_name', '')
        )
        return user