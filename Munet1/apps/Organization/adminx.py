__author__ = 'Pei'
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['city_name', 'add_time']
    list_filter = ['city_name', 'add_time']
    search_fields = ['city_name']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'collection_nums',
                    'Org_image', 'address', 'city', 'add_time']
    list_filter = ['name', 'desc', 'click_nums', 'collection_nums',
                   'Org_image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'collection_nums',
                     'Org_image', 'address', 'city']


class TeacherAdmin(object):
    list_display = ['course_org', 'name', 'work_years', 'work_company',
                    'work_position', 'point', 'click_nums','collection_nums', 'add_time']
    list_filter = ['course_org', 'name', 'work_years', 'work_company',
                   'work_position', 'point', 'click_nums', 'collection_nums', 'add_time']
    search_fields = ['course_org', 'name', 'work_years', 'work_company',
                     'work_position', 'point', 'click_nums', 'collection_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
