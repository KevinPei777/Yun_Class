# Generated by Django 2.0.4 on 2018-05-06 13:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=20, verbose_name='城市名')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='机构名称')),
                ('desc', models.TextField(verbose_name='机构描述')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('collection_nums', models.IntegerField(default=0, verbose_name='收藏人数')),
                ('Org_image', models.ImageField(upload_to='image/orgs', verbose_name='机构封面')),
                ('address', models.CharField(default='', max_length=150, verbose_name='机构地址')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organization.CityDict', verbose_name='城市')),
            ],
            options={
                'verbose_name': '课程机构',
                'verbose_name_plural': '课程机构',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='教师名称')),
                ('work_years', models.IntegerField(default=0, verbose_name='工作年龄')),
                ('work_company', models.CharField(max_length=50, verbose_name='公司')),
                ('work_position', models.CharField(max_length=50, verbose_name='职位')),
                ('point', models.CharField(max_length=50, verbose_name='教学特点')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('collection_nums', models.IntegerField(default=0, verbose_name='收藏人数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organization.CourseOrg', verbose_name='所属机构')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
        ),
    ]