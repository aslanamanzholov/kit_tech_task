from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TasksSerializer, ChangeTaskStatusSerializer


class TaskViews(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer

    def perform_create(self, serializer):
        created_by = self.request.user
        serializer.save(created_by=created_by)

    def perform_update(self, serializer):
        edited_by = self.request.user
        serializer.save(edited_by=edited_by)

    def get_serializer_class(self):
        if self.action == 'task_status_change':
            return ChangeTaskStatusSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=False)
    def task_status_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            task = Task.objects.get(id=request.data['task'])
            task.status = request.data['status']
            task.before_task_status = request.data['before_task_status']
            task.edited_by = self.request.user
            task.save()
            return Response({'detail': "OK"}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'detail': 'id is not set'})