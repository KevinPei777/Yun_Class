# Generated by Django 2.0.5 on 2018-05-21 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0002_auto_20180521_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='class_image',
            field=models.ImageField(upload_to='image/courses', verbose_name='课程封面'),
        ),
    ]
