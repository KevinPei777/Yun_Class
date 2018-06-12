__author__ = 'Pei'
import xadmin

from .models import Course, CourseResource, Lesson, Vedio


# 与下方的inline关联
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'difficulty', 'learn_times', 'students',
                    'collection_nums', 'class_image', 'click_nums', 'add_time']
    list_filter = ['name', 'desc', 'detail', 'difficulty', 'learn_times', 'students',
                   'collection_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'difficulty', 'students',
                     'collection_nums', 'click_nums']
    inlines = [LessonInline]
    # list_editable = []  在列表页进行编辑
    # refresh_time = [] 对列表页自动刷新


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    list_filter = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    list_filter = ['course__name', 'name', 'add_time']
    search_fields = ['course', 'name']


class VedioAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    list_filter = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Vedio, VedioAdmin)
xadmin.site.register(Lesson, LessonAdmin)