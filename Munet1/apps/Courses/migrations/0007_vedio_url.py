# Generated by Django 2.0.5 on 2018-06-01 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0006_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='vedio',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='访问链接'),
        ),
    ]
