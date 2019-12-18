from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id', 'is_admin')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        return super(UserSerializer, self).update(instance, validated_data)


class UserHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserHistory
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class BlockUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockUser
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
