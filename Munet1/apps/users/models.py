from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 用户信息
class UserData(AbstractUser):
    nick_name = models.CharField(max_length=30, default='', verbose_name=u'昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    gender = models.CharField(max_length=10, choices=(('male', "男"), ("female", "女")),
                              default='female', verbose_name=u'性别')
    address = models.CharField(max_length=100, default="", verbose_name=u'地址')
    mobile_num = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'手机号')
    image = models.ImageField(upload_to='image/users', max_length=100,
                              default='image/users/default.png', verbose_name=u'用户头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_message_count(self):
        from Operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


# 邮箱验证
class EmailVerifyRecord(models.Model):
    verify_code = models.CharField(max_length=30, verbose_name=u'验证码')
    email = models.EmailField(max_length=30, verbose_name=u"邮箱")
    send_type = models.CharField(max_length=15, choices=(('register', u"注册"), ("forget", u"找回密码"),
                                                         ("update_email", "修改邮箱")), verbose_name=u'提交类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'提交时间')

    class Meta:
        verbose_name = u"验证邮箱"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}\t验证类型:{1}'.format(self.email, self.send_type)


# 轮播图
class Banner(models.Model):
    title = models.CharField(max_length=20, verbose_name=u"标题")
    image = models.ImageField(max_length=100, upload_to='BannerImage', verbose_name=u'图片')
    url = models.URLField(max_length=200, verbose_name=u'url')
    index = models.IntegerField(default=1, verbose_name=u"图片索引")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
