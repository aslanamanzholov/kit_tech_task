from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'last_login', 'date_joined', 'groups', 'user_permissions')
