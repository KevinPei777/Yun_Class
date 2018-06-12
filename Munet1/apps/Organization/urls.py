from django.urls import re_path
from .views import OrgView, AddUserAskView, OrgHomepageView, OrgCourseView
from .views import OrgDescView, OrgTeacherView, OrgCollection, TeacherListView, TeacherDetailView

urlpatterns = [
    re_path(r'^org/$', OrgView.as_view(), name='org_list'),
    re_path(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    re_path(r'^org_homepage/(?P<org_id>\d+)/$', OrgHomepageView.as_view(), name='org_homepage'),
    re_path(r'^org_courses/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    re_path(r'^org_desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    re_path(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    re_path(r'^add_collection/$', OrgCollection.as_view(), name='add_collection'),

    # 讲师url
    re_path(r'^teacher_list/$', TeacherListView.as_view(), name='teacher_list'),
    re_path(r'^teacher_detail/(?P<teacher_id>\d+)/$',TeacherDetailView.as_view(), name='teacher_detail')
]
