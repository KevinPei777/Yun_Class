# Generated by Django 2.0.5 on 2018-06-02 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0009_auto_20180526_1059'),
        ('Courses', '0008_vedio_video_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Organization.Teacher', verbose_name='课程讲师'),
        ),
    ]