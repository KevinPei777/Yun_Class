from datetime import datetime

from django.db import models
from users.models import UserData
from Courses.models import Course
# Create your models here.


# 用户咨询
class UserAsk(models.Model):
    user_name = models.CharField(max_length=20, verbose_name=u'用户姓名')
    mobile_nums = models.CharField(max_length=11, verbose_name=u'手机号')
    course_name = models.CharField(max_length=50, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name


# 课程评论
class CourseComments(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, verbose_name=u'用户名')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程名')
    comments = models.CharField(max_length=200, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def __str__(self):
        return self.comments

    class Meta:
        verbose_name = u'评论信息'
        verbose_name_plural = verbose_name


# 用户收藏
class UserCollections(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, verbose_name=u'用户名')
    collection_id = models.IntegerField(default=0, verbose_name=u'数据id')
    collection_type = models.IntegerField(choices=((1, u'课程'), (2, u'机构'), (3, u'讲师')),
                                          default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户收藏信息'
        verbose_name_plural = verbose_name


# 用户消息
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接受用户')
    message = models.CharField(max_length=300, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


# 用户课程
class UserCourse(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, verbose_name=u'用户名')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name
