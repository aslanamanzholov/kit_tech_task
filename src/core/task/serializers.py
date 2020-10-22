from rest_framework import serializers

from .models import Task
from ..users.serializers import UserSerializer


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