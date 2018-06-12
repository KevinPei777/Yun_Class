from django.urls import re_path
from users.views import UserInfoView, UploadImageView, ChangePwdView
from users.views import SendChangeEmailView, ChangeEmailView, MyCourseView
from users.views import MyOrgCollectionView, MyTeacherCollectionView, MyCourseCollectionView, MyMessageView

urlpatterns = [
    re_path(r'^center_info/$', UserInfoView.as_view(), name='center_info'),
    re_path(r'^my_course/$', MyCourseView.as_view(), name='my_course'),

    # 我的收藏
    re_path(r'^my_collection/orgs/$', MyOrgCollectionView.as_view(), name='collections_orgs'),
    re_path(r'^my_collection/teachers/$', MyTeacherCollectionView.as_view(), name='collections_teachers'),
    re_path(r'^my_collection/courses/$', MyCourseCollectionView.as_view(), name='collections_courses'),
    # 我的消息
    re_path(r'^my_message/$', MyMessageView.as_view(), name='my_message'),
    # 上传头像
    re_path(r'^image_upload/$', UploadImageView.as_view(), name='image_upload'),

    # 修改密码
    re_path(r'^change_pwd/$', ChangePwdView.as_view(), name='change_pwd'),

    # 发送修改邮箱验证码
    re_path(r'^send_email/$', SendChangeEmailView.as_view(), name='send_email'),
    # 修改邮箱验证码
    re_path(r'^change_email/$', ChangeEmailView.as_view(), name='change_email'),

]
