from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=password,
        )

        if password is not None:
            user.set_password(password)

        user.save()

        return user

