from datetime import datetime

from django.db import models


# Create your models here.
# 城市
class CityDict(models.Model):
    city_name = models.CharField(max_length=20, verbose_name=u'城市名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name


# 机构信息
class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(max_length=15, choices=(('colleges', '高校'), ('personal', '个人'), ('orgs', '培训机构')),
                                default='orgs', verbose_name='机构类别')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    collection_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    Org_image = models.ImageField(upload_to='image/orgs', verbose_name=u'机构封面')
    address = models.CharField(max_length=150, default="", verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE,verbose_name=u'城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    students = models.IntegerField(default=0, verbose_name=u'学生数量')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数量')
    tag = models.CharField(max_length=8, default='权威机构', verbose_name='机构标签')

    def __str__(self):
        return self.name

    def get_teachers(self):
        return self.teacher_set.all().count()

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name


# 教师信息
class Teacher(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE,verbose_name=u'所属机构')
    name = models.CharField(max_length=20, verbose_name=u'教师名称')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年龄')
    work_company = models.CharField(max_length=50, verbose_name=u'公司')
    work_position = models.CharField(max_length=50, verbose_name=u'职位')
    teacher_image = models.ImageField(upload_to='image/orgs/teachers', verbose_name='教师头像')
    point = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    collection_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def __str__(self):
        return self.name

    # 获取教师课程数
    def get_courses(self):
        return self.course_set.all().count()

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name
