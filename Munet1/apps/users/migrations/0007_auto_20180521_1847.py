# Generated by Django 2.0.5 on 2018-05-21 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180521_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='image',
            field=models.ImageField(default='image/users/default.png', upload_to='image/users', verbose_name='用户头像'),
        ),
    ]