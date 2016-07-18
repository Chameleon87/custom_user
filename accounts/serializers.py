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


class AuthTokenSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    user_type = serializers.SerializerMethodField()

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data
