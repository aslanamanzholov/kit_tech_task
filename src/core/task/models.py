from django.conf import settings
from django.db import models

from ..helpers.constants import TASK_STATUS


class Task(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Описание')
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name='Исполнители', related_name='executor')
    observers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name='Наблюдатели',
                                       related_name='observers')
    status = models.CharField(max_length=255, choices=TASK_STATUS, blank=False, null=True, verbose_name='Статус')
    start_time = models.DateTimeField(blank=False, null=True, verbose_name='Время начало')
    end_time = models.DateTimeField(blank=False, null=True, verbose_name='Время завершения')
    planned_completion_time = models.DateTimeField(blank=False, null=True, verbose_name='Планируемое время завершения')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False,
                                   verbose_name='Пользователь', related_name='created_by')
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Редактируемый пользователь', related_name='edited_by')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-start_time']
        db_table = "task_db"

    def __str__(self):
        return '{}'.format(self.name)
