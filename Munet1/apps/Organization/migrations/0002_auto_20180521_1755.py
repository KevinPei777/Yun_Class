# Generated by Django 2.0.5 on 2018-05-21 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='Org_image',
            field=models.ImageField(upload_to='media/image/orgs', verbose_name='机构封面'),
        ),
    ]