# Generated by Django 2.2.8 on 2020-10-22 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0003_task_before_task_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationForUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_of_notification', models.CharField(blank=True, max_length=255, null=True, verbose_name='Текст уведомлении')),
                ('notification_for_users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Пользователи для уведомления')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.Task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомлении',
                'db_table': 'notification_db',
                'ordering': ['-task'],
            },
        ),
    ]
