from datetime import datetime

from django.db import models

from Organization.models import CourseOrg, Teacher

# Create your models here.


# 课程表
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='课程机构', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=u"课程名")
    desc = models.CharField(max_length=200, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u'课程详情')
    category = models.CharField(max_length=20, default='', verbose_name='课程类别')
    difficulty = models.CharField(max_length=10,
                                  choices=(('ezsy', u'简单'), ('mid', u'中等'),
                                           ('difficult', u"困难")),
                                  verbose_name=u'课程难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'分钟数')
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    collection_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    class_image = models.ImageField(upload_to='image/courses', verbose_name=u'课程封面')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    tag = models.CharField(default='', max_length=15, verbose_name='课程标签')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='课程讲师', null=True, blank=True)
    course_required = models.CharField(max_length=100, default='', verbose_name='课程须知')
    teacher_message = models.CharField(max_length=100, default='', verbose_name='教师告诉你')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取课程章节数
    def get_lesson_count(self):
        return self.lesson_set.all().count()

    # 获取章节信息
    def get_lesson(self):
        return self.lesson_set.all()


# 章节表
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        return self.vedio_set.all()

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name


# 视频表
class Vedio(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, default='', verbose_name='访问链接')
    video_times = models.IntegerField(default=0, verbose_name=u'分钟数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'课程视频'
        verbose_name_plural = verbose_name


# 下载资源表
class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    download = models.FileField(max_length=100, upload_to='course/resource', verbose_name=u'资源文件')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
