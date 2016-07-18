from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from models import AcUser

USER_TYPES = (
    ( 'customer', 'Customer'),
    ( 'courier', 'Courier'),
)

class AcUserSerializer(ModelSerializer):

    class Meta:
        model = AcUser
        fields = ['user_type', 'email', 'password']
        write_only_fields = ['password']
        read_only_fields = ['id']

    def get_user_type(self, user_type):
        return user_type

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


class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()
    user_type = serializers.SerializerMethodField

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')
        user_type = attrs.get('user_type')

        if email_or_username and password:
            # Check if user sent email
            if validateEmail(email_or_username):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
