from rest_framework import viewsets

from .models import Task
from .serializers import TasksSerializer


class TaskViews(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer

    def perform_create(self, serializer):
        created_by = self.request.user
        serializer.save(created_by=created_by)

    def perform_update(self, serializer):
        edited_by = self.request.user
        serializer.save(edited_by=edited_by)
