from django.urls import re_path

from .views import CourseView, CourseDetailsView, CourseVideoView,\
                   CourseCommentView, AddCourseCommentView, CoursePlayView

urlpatterns = [
    re_path(r'^$', CourseView.as_view(), name='course_list'),
    re_path(r'^course_detail/(?P<course_id>\d+)/$', CourseDetailsView.as_view(), name='course_detail'),
    re_path(r'^course_detail/(?P<course_id>\d+)/course_video/$', CourseVideoView.as_view(), name='course_video'),
    re_path(r'^course_detail/(?P<course_id>\d+)/course_comment/$', CourseCommentView.as_view(), name='course_comment'),
    re_path(r'^course_play/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name='course_play'),
    # 添加课程评论
    re_path(r'^add_comment/$', AddCourseCommentView.as_view(), name='add_comment')
]