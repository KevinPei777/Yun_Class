# Generated by Django 2.0.4 on 2018-05-06 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Courses', '0001_initial'),
        ('Operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='usercollections',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='coursecomments',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.Course', verbose_name='课程名'),
        ),
        migrations.AddField(
            model_name='coursecomments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
    ]
