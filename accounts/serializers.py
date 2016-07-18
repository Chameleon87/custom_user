from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from models import AcUser

USER_TYPES = (
    ( 'customer', 'Customer'),
    ( 'courier', 'Courier'),
)

class AcUserSerializer(ModelSerializer):
    user_type = serializers.CharField()

    class Meta:
        model = AcUser
        fields = ['user_type', 'email', 'password']
        write_only_fields = ['password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
