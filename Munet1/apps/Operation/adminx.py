__author__ = 'Pei'
import xadmin

from .models import UserAsk, UserCollections, UserMessage, CourseComments, UserCourse


class UserAskAdmin(object):
    list_display = ['user_name', 'mobile_nums', 'course_name', 'add_time']
    list_filter = ['user_name', 'mobile_nums', 'course_name', 'add_time']
    search_fields = ['user_name', 'mobile_nums', 'course_name']


class UserCollectionsAdmin(object):
    list_display = ['user', 'collection_id', 'collection_type', 'add_time']
    list_filter = ['user', 'collection_id', 'collection_type', 'add_time']
    search_fields = ['user', 'collection_id', 'collection_type']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    list_filter = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']


xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCollections, UserCollectionsAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)