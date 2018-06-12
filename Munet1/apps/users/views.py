from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse

import json

from users.models import UserData, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UploadImageForm, UpdateInfoForm
from utils.send_email import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from Operation.models import UserCourse, UserCollections, UserMessage
from Organization.models import CourseOrg, Teacher
from Courses.models import Course


class CustomBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserData.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.
# 用户登陆逻辑类
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_forms = LoginForm(request.POST)
        if login_forms.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active is True:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '账户未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！',
                                                      "login_forms": login_forms})
        else:
            return render(request, 'login.html', {"login_forms": login_forms})


# 用户退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 用户注册类
class RegisterView(View):
    def get(self, request):
        register_forms = RegisterForm()
        return render(request, 'register.html', {'register_forms': register_forms})

    def post(self, request):
        register_forms = RegisterForm(request.POST)
        if register_forms.is_valid():
            user_name = request.POST.get('email', '')
            if UserData.objects.filter(email=user_name):
                return render(request, 'register.html',
                              {'msg': '用户名已存在！', 'register_forms': register_forms})
            pass_word = request.POST.get('password', '')
            user_data = UserData()
            user_data.username = user_name
            user_data.email = user_name
            user_data.password = make_password(pass_word)
            user_data.is_active = False
            user_data.save()
            send_register_email(user_name, 'register')
            # 写入欢迎注册
            user_message = UserMessage()
            user_message.user = user_data.id
            user_message.message = '欢迎来到在线云课堂！'
            user_message.save()
            return render(request, 'email_return.html')
        else:
            return render(request, 'register.html', {'register_forms': register_forms})


# 激活注册
class ActiveUserView(View):
    def get(self, request, active_code):
        all_verify_record = EmailVerifyRecord.objects.filter(verify_code=active_code)
        if all_verify_record:
            email = all_verify_record[0].email
            user = UserData.objects.get(email=email)
            user.is_active = True
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'actice_fail.html')


# 找回密码
class ForgetPwdView(View):
    def get(self, request):
        forget_forms = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_forms': forget_forms})

    def post(self, request):
        forget_forms = ForgetPwdForm(request.POST)
        if forget_forms.is_valid():
            email = request.POST.get('email')
            if UserData.objects.filter(email=email):
                send_register_email(email, 'forget')
                return render(request, 'email_return.html')
            else:
                return render(request, 'forgetpwd.html', {'forget_forms': forget_forms,
                                                          'msg': '该帐号不存在，请重新输入'})
        return render(request, 'forgetpwd.html', {'forget_forms': forget_forms})


# 验证及重置密码
class ResetView(View):
    def get(self, request, reset_code):
        verify_code = EmailVerifyRecord.objects.filter(verify_code=reset_code)
        if verify_code:
            email = verify_code[0].email
            return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'actice_fail.html')


class ModifyPwdView(View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        email = request.POST.get('email')
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 == pwd2:
                user = UserData.objects.get(email=email)
                user.password = make_password(pwd1)
                user.save()
                return render(request, 'login.html')
            else:
                return render(request, 'password_reset.html', {'email': email,
                                                               'msg': '两次输入不一致，请重新输入'})
        else:
            return render(request, 'password_reset.html', {'email': email, 'reset_form': reset_form})


# 个人中心
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        cur_page = 'center_info'
        return render(request, 'usercenter-info.html', {
            'cur_page': cur_page
        })

    def post(self, request):
        update_form = UpdateInfoForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(update_form.errors), content_type='application/json')


# 上传头像
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fails"}', content_type='application/json')


# 修改密码
class ChangePwdView(LoginRequiredMixin, View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 == pwd2:
                user = request.user
                user.password = make_password(pwd1)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"两次密码不一致"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


# 发送修改邮箱
class SendChangeEmailView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserData.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


# 修改邮箱
class ChangeEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')

        db_code = EmailVerifyRecord.objects.filter(email=email, verify_code=code, send_type='update_email')
        if db_code:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"邮箱验证失败"}', content_type='application/json')


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        cur_page = 'my_course'
        courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'cur_page': cur_page,
            'courses': courses
        })


# 我的收藏
class MyOrgCollectionView(LoginRequiredMixin, View):
    def get(self, request):
        cur_page = 'my_collection'
        org_list = []
        collection_orgs = UserCollections.objects.filter(user=request.user, collection_type=2)
        for orgs in collection_orgs:
            org = CourseOrg.objects.get(id=orgs.collection_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'cur_page': cur_page,
            'org_list': org_list
        })


class MyTeacherCollectionView(LoginRequiredMixin, View):
    def get(self, request):
        cur_page = 'my_collection'
        teacher_list = []
        collection_teachers = UserCollections.objects.filter(user=request.user, collection_type=3)
        for teachers in collection_teachers:
            teacher = Teacher.objects.get(id=teachers.collection_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'cur_page': cur_page,
            'teacher_list': teacher_list
        })


class MyCourseCollectionView(LoginRequiredMixin, View):
    def get(self, request):
        cur_page = 'my_collection'
        course_list = []
        collection_courses = UserCollections.objects.filter(user=request.user, collection_type=1)
        for courses in collection_courses:
            course = Course.objects.get(id=courses.collection_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'cur_page': cur_page,
            'course_list': course_list
        })


# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        cur_page = 'my_message'
        all_message = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')

        # 分页
        paginator = Paginator(all_message, 5)
        page = request.GET.get('page', 1)
        try:
            message = paginator.page(page)
        except EmptyPage:
            message = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            message = paginator.page(1)
        for mess in all_message:
            mess.has_read = True
            mess.save()

        return render(request, 'usercenter-message.html', {
            'cur_page': cur_page,
            'message': message
        })


# 首页
class IndexView(View):
    def get(self, request):
        # 轮播图
        all_banners = Banner.objects.all().order_by('index')

        # 课程
        all_courses = Course.objects.all()[:6]
        # 广告图
        ad_course_banner = Course.objects.all().order_by('click_nums')[:2]

        # 机构
        all_orgs = CourseOrg.objects.all()

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'ad_course_banner': ad_course_banner,
            'all_orgs': all_orgs,
            'all_courses': all_courses
        })


# 404
def page_404(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 500
def page_500(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
