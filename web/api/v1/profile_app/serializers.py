from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'full_name', 'last_name', 'email', 'birthday', 'gender', 'avatar', 'count_articles', 'count_comments')


class ProfileUpdateBIOSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday', 'gender')



class ProfileUpdatePasswordSerializer(serializers.ModelSerializer):
    password_1 = serializers.CharField(write_only=True, min_length=8)
    password_2 = serializers.CharField(write_only=True, min_length=8)
    old_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('old_password', 'password_1', 'password_2')

    def validate_old_password(self, old_password: str) -> str:
        if not self.context['request'].user.check_password(old_password):
            raise serializers.ValidationError(_('The old password wrong'))
        return old_password

    def validate_password_1(self, password: str):
        validate_password(password)
        return password

    def validate(self, data):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError(_('The two password fields did not match'))
        return data



class ProfileUpdateAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('avatar', )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar', 'full_name', 'is_active', 'date_joined', 'email', 'id')
