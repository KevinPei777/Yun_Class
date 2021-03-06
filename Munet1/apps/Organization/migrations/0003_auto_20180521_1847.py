# Generated by Django 2.0.5 on 2018-05-21 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0002_auto_20180521_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(default='培训机构', max_length=15, verbose_name='机构类别'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='Org_image',
            field=models.ImageField(upload_to='image/orgs', verbose_name='机构封面'),
        ),
    ]
