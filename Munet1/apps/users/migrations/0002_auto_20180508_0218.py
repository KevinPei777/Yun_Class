# Generated by Django 2.0.4 on 2018-05-08 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='"female', max_length=10, verbose_name='性别'),
        ),
    ]
