# Generated by Django 2.0.5 on 2018-05-26 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0008_auto_20180526_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='teacher_image',
            field=models.ImageField(upload_to='image/orgs/teachers', verbose_name='教师头像'),
        ),
    ]
