from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponse
from django.db.models import Q

from Courses.models import Course, CourseResource, Vedio
from Operation.models import UserCollections, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.
class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        # 按热门筛选
        high_click = all_courses.order_by('-click_nums')[:4]

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords)
                                             | Q(detail__icontains=search_keywords) | Q(course_org__name__icontains=search_keywords))

        # 排序
        sort_course = request.GET.get('sort', '')
        if sort_course:
            if sort_course == 'students':
                all_courses = all_courses.order_by('-students')
            if sort_course == 'hot':
                all_courses = all_courses.order_by('-click_nums')
        # 分页
        paginator = Paginator(all_courses, 3)
        page = request.GET.get('page', 1)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        return render(request, 'course-list.html', {
            'all_courses': all_courses,
            'courses': courses,
            'sort_course': sort_course,
            'high_click': high_click,
        })


# 课程详情
class CourseDetailsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()

        # 收藏
        has_collection_course = False
        has_collection_org = False
        if request.user.is_authenticated:
            if UserCollections.objects.filter(user=request.user, collection_id=course.id, collection_type=1):
                has_collection_course = True
            if UserCollections.objects.filter(user=request.user, collection_id=course.course_org.id, collection_type=2):
                has_collection_org = True

        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'has_collection_course': has_collection_course,
            'has_collection_org': has_collection_org
        })


# 课程视频列表
class CourseVideoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        # 课程与同学级联，增加学习人数
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            course.students += 1
            course.save()
            user_course.save()

        # 通过学习同学推荐
        course_students = UserCourse.objects.filter(course=course)
        user_ids = [user.user.id for user in course_students]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [id_course.course.id for id_course in all_user_courses]
        recommend_course = Course.objects.filter(id__in=course_ids).order_by('-students')[:3]

        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_id': course_id,
            'all_resource': all_resource,
            'recommend_course': recommend_course
        })


# 课程评论
class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        # 通过学习同学推荐
        course_students = UserCourse.objects.filter(course=course)
        user_ids = [user.user.id for user in course_students]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [id_course.course.id for id_course in all_user_courses]
        recommend_course = Course.objects.filter(id__in=course_ids).order_by('-students')[:3]

        all_resource = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'course_id': course_id,
            'all_comments': all_comments,
            'all_resource': all_resource,
            'recommend_course': recommend_course
        })


# 添加评论
class AddCourseCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"请进行登陆"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comment', '')
        if int(course_id) > 0 and comment != '':
            course_comment = CourseComments()
            course_comment.course = Course.objects.get(id=course_id)
            course_comment.user = request.user
            course_comment.comments = comment
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功!"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success","msg":"评论失败!"}', content_type='application/json')


# 课程播放页面
class CoursePlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Vedio.objects.get(id=video_id)
        course = video.lesson.course

        # 通过学习同学推荐
        course_students = UserCourse.objects.filter(course=course)
        user_ids = [user.user.id for user in course_students]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [id_course.course.id for id_course in all_user_courses]
        recommend_course = Course.objects.filter(id__in=course_ids).order_by('-students')[:3]

        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resource': all_resource,
            'recommend_course': recommend_course,
            'video': video
        })
