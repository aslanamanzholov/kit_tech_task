import json

from celery import Celery
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TasksSerializer, ChangeTaskStatusSerializer, NotificationForUserSerializer
from ..schedules import send_email, send_email_for_user
from ..users.serializers import UserSerializer

app = Celery('core')
User = get_user_model()


class TaskViews(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        created_by = self.request.user
        serializer.save(created_by=created_by)

    def perform_update(self, serializer):
        edited_by = self.request.user
        serializer.save(edited_by=edited_by)

    def get_serializer_class(self):
        if self.action == 'task_status_change':
            return ChangeTaskStatusSerializer
        elif self.action == 'send_notification_for_user':
            return NotificationForUserSerializer
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
            if task.observers is not None:
                for i in task.observers.all():
                    celery_task = app.task(send_email).apply(args=[i.id, i.first_name,
                                                                   i.last_name, i.email, request.data['status'],
                                                                   request.data['before_task_status']])
                    print(f"id={celery_task.id}, state={celery_task.state}, status={celery_task.status}")
            return Response({'detail': "OK"}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "input doesn't set"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def send_notification_for_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            test = list(serializer['users'].value)
            task = request.data['task']
            text_of_notification = request.data['text_of_notification']
            print(text_of_notification)
            for i in test:
                user = User.objects.get(id=i)
                celery_task = app.task(send_email_for_user).apply(args=[user.id, user.first_name,
                                                                        user.last_name, user.email,
                                                                        text_of_notification,
                                                                        task])
                print(f"id={celery_task.id}, state={celery_task.state}, status={celery_task.status}")
            return Response({'detail': "OK"}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "input doesn't set"}, status=status.HTTP_400_BAD_REQUEST)

# class NotificationForUserViewSet(viewsets.ModelViewSet):
#     queryset = NotificationForUser.objects.all()
#     serializer_class = NotificationForUserSerializer
#     permission_classes = (IsAuthenticated,)
