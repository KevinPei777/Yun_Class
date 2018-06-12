from django.shortcuts import render
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from Organization.models import CourseOrg, CityDict, Teacher
from Operation.models import UserCollections
from .forms import UserAskForm
from Courses.models import Course


# Create your views here.
class OrgView(View):
    # 授课机构首页功能类
    def get(self, request):
        cur_page = 'orgs'
        all_orgs = CourseOrg.objects.all().order_by('id')
        all_city = CityDict.objects.all()
        # 级联机构课程数与学生人数
        for org in all_orgs:
            org.course_nums = org.course_set.filter(course_org_id=org.id).count()
            students = 0
            for count in org.course_set.filter(course_org_id=org.id):
                students += count.students
            org.students = students
            org.save()
        # 按点击量取出机构
        high_click = all_orgs.order_by('click_nums')[:3]

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 筛选机构类别类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 排序
        sort_orgs = request.GET.get('sort', '')
        if sort_orgs:
            if sort_orgs == 'students':
                all_orgs = all_orgs.order_by('-students')
            if sort_orgs == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')
        # 分页课程机构
        paginator = Paginator(all_orgs, 2)
        page = request.GET.get('page')

        org_count = all_orgs.count()
        try:
            orgs = paginator.page(page)
        except PageNotAnInteger:
            orgs = paginator.page(1)
        except EmptyPage:
            orgs = paginator.page(paginator.num_pages)
        return render(request, 'org-list.html',
                      {'orgs': orgs,
                       'all_city': all_city,
                       'org_count': org_count,
                       'city_id': city_id,
                       'category': category,
                       'high_click': high_click,
                       'sort_orgs': sort_orgs,
                       'cur_page': cur_page
                       })


# 用户咨询类
class AddUserAskView(View):
    def post(self, request):
        ask_form = UserAskForm(request.POST)
        if ask_form.is_valid():
            user_ask = ask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"失败，请检查您的信息"}', content_type='application/json')


# 机构详情页面
class OrgHomepageView(View):
    def get(self, request, org_id):
        current_page = 'OrgHomepage'
        has_collection = False
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        if request.user.is_authenticated:
            if UserCollections.objects.filter(user=request.user, collection_id=course_org.id, collection_type=2):
                has_collection = True
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-homepage.html',
                      {'all_courses': all_courses[:4],
                       'all_teachers': all_teachers[:3],
                       'course_org': course_org,
                       'current_page': current_page,
                       'has_collection': has_collection,
                       })


# 机构课程页面
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'OrgCourse'
        has_collection = False
        course_org = CourseOrg.objects.get(id=int(org_id))
        if request.user.is_authenticated:
            if UserCollections.objects.filter(user=request.user, collection_id=course_org.id, collection_type=2):
                has_collection = True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html',
                      {'all_courses': all_courses,
                       'course_org': course_org,
                       'current_page': current_page,
                       'has_collection': has_collection,
                       })


# 机构介绍
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'OrgDesc'
        has_collection = False
        course_org = CourseOrg.objects.get(id=int(org_id))
        if request.user.is_authenticated:
            if UserCollections.objects.filter(user=request.user, collection_id=course_org.id, collection_type=2):
                has_collection = True
        return render(request, 'org-detail-desc.html',
                      {'course_org': course_org,
                       'current_page': current_page,
                       'has_collection': has_collection,
                       })


# 机构教师
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'OrgTeacher'
        has_collection = False
        course_org = CourseOrg.objects.get(id=int(org_id))
        if request.user.is_authenticated:
            if UserCollections.objects.filter(user=request.user, collection_id=course_org.id, collection_type=2):
                has_collection = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',
                      {
                       'all_teachers': all_teachers,
                       'course_org': course_org,
                       'current_page': current_page, 'has_collection': has_collection,
                       })


# 收藏机构
class OrgCollection(View):
    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"请进行登陆"}', content_type='application/json')
        # 通过记录是否存在判断是否收藏
        record = UserCollections.objects.filter(user=request.user, collection_id=fav_id, collection_type=fav_type)
        if record:
            if fav_type == 1:
                course = Course.objects.get(id=fav_id)
                course.collection_nums -= 1
                course.save()
            elif fav_type == 2:
                course_org = CourseOrg.objects.get(id=fav_id)
                course_org.collection_nums -= 1
                course_org.save()
            elif fav_type == 3:
                teacher = Teacher.objects.get(id=fav_id)
                teacher.collection_nums -= 1
                teacher.save()
            record.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        elif fav_id > 0 and fav_type > 0:
            user_collection = UserCollections()
            user_collection.user = request.user
            user_collection.collection_id = fav_id
            user_collection.collection_type = fav_type
            user_collection.save()
            if fav_type == 1:
                course = Course.objects.get(id=fav_id)
                course.collection_nums += 1
                course.save()
            elif fav_type == 2:
                course_org = CourseOrg.objects.get(id=fav_id)
                course_org.collection_nums += 1
                course_org.save()
            elif fav_type == 3:
                teacher = Teacher.objects.get(id=fav_id)
                teacher.collection_nums += 1
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')


# 讲师首页
class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all().order_by('id')
        # 排序
        sort_teachers = request.GET.get('sort', '')
        if sort_teachers:
            if sort_teachers == 'hot':
                teachers = teachers.order_by('-click_nums')
        # 讲师排行榜
        rank_teachers = teachers.order_by('-click_nums')[:3]

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            teachers = teachers.filter(Q(name__icontains=search_keywords) | Q(point__icontains=search_keywords))

        # 对教师分页
        paginator = Paginator(teachers, 3)
        page = request.GET.get('page')

        try:
            teacher = paginator.page(page)
        except PageNotAnInteger:
            teacher = paginator.page(1)
        except EmptyPage:
            teacher = paginator.page(paginator.num_pages)

        return render(request, 'teachers-list.html', {
            'teacher': teacher,
            'sort_teachers': sort_teachers,
            'rank_teachers': rank_teachers
        })


# 讲师详情
class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        teacher_course = teacher.course_set.filter(teacher=teacher_id)

        # 讲师排行榜
        rank_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        has_collection_teacher = False
        has_collection_org = False
        if UserCollections.objects.filter(user=request.user, collection_id=teacher_id, collection_type=3):
            has_collection_teacher = True
        if UserCollections.objects.filter(user=request.user, collection_id=teacher.course_org.id, collection_type=2):
            has_collection_org = True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'teacher_course': teacher_course,
            'rank_teachers': rank_teachers,
            'has_collection_teacher': has_collection_teacher,
            'has_collection_org': has_collection_org
        })
