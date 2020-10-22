from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .task.models import Task


@shared_task
def send_email(id, first_name, last_name, email, status, before_task_status, **kwargs):
    send_mail(
        subject='Изменение статуса задачи',
        message=f'{first_name} {last_name}, статус задачи изменен с {before_task_status} на {status}',
        from_email='site@no-reply.kz',
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def send_email_for_user(id, first_name, last_name, email, text_of_notification, task, **kwargs):
    send_mail(
        subject='Изменение статуса задачи',
        message=f'{first_name} {last_name}, Идентификатор Задачи: {task}, Текст уведомлении: {text_of_notification}',
        from_email='site@no-reply.kz',
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def send_email_to_executor(**kwargs):
    task = Task.objects.all()
    for i in task:
        if i.end_time <= timezone.now() and i.executor.email is not None:
            send_mail(
                subject='Изменение статуса задачи',
                message=f'{i.executor.first_name} {i.executor.last_name}, задача устарела',
                from_email='site@no-reply.kz',
                recipient_list=[i.executor.email],
                fail_silently=False,
            )
