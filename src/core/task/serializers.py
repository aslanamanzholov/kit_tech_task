from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Task
from ..helpers.constants import TASK_STATUS
from ..users.serializers import UserSerializer

User = get_user_model()


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_by', 'edited_by')

    def to_representation(self, instance):
        representation = super(TasksSerializer, self).to_representation(instance)
        if instance.executor is not None:
            representation['executor'] = UserSerializer(instance.executor).data
        if instance.created_by is not None:
            representation['created_by'] = UserSerializer(instance.created_by).data
        if instance.edited_by is not None:
            representation['edited_by'] = UserSerializer(instance.edited_by).data
        if instance.observers is not None:
            representation['observers'] = UserSerializer(instance.observers, many=True).data
        return representation


class ChangeTaskStatusSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    before_task_status = serializers.ChoiceField(choices=TASK_STATUS)

    class Meta:
        model = Task
        fields = ('before_task_status', 'status', 'edited_by', 'task')
        read_only_fields = ('edited_by',)


class NotificationForUserSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    text_of_notification = serializers.CharField(max_length=250, allow_blank=True)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Task
        fields = ('task', 'text_of_notification', 'users',)

# class NotificationForUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NotificationForUser
#         fields = '__all__'
