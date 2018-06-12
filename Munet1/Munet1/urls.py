"""Munet1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin


from django.urls import path, re_path, include
from django.views.static import serve
from .settings import MEDIA_ROOT
# , STATIC_ROOT

from users.views import LoginView, RegisterView, ActiveUserView, IndexView
from users.views import ForgetPwdView, ResetView, ModifyPwdView, LogoutView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 登陆类url
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^register/$', RegisterView.as_view(), name='register'),
    re_path(r'^forget/$',  ForgetPwdView.as_view(), name='forget'),

    # captcha库
    re_path(r'^captcha/', include('captcha.urls')),

    # 邮箱激活验证链接
    re_path(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    re_path(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='user_reset'),
    # re_path(r'^update_email/(?P<reset_code>.*)/$', ResetView.as_view(), name='user_reset'),
    re_path(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 讲师url
    re_path(r'^teacher/', include('Organization.urls')),

    # 课程机构url
    re_path(r'^org_list/', include('Organization.urls')),

    # 配置上传文件访问处理
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    # 公开课首页
    re_path(r'^course_list/', include('Courses.urls')),

    # 个人中心
    re_path(r'^user/', include('users.urls')),
]


# 全局404
handler404 = 'users.views.page_404'
# 全局500
handler500 = 'users.views.page_500'
