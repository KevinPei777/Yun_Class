from django import forms
from captcha.fields import CaptchaField

from users.models import UserData


# 用户登陆验证表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '帐号不能为空'})
    password = forms.CharField(required=True, min_length=6,
                               error_messages={'required': '密码不能为空',
                                               'min_length': '密码最小长度为6'})


# 用户注册验证表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': '帐号不能为空'})
    password = forms.CharField(required=True, min_length=6, max_length=20,
                               error_messages={'required': '密码不能为空',
                                               'min_length': '密码最小长度为6',
                                               'max_length': '密码最大长度为20'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误',
                                           'required': '验证码不能为空'})


# 找回密码表单
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误',
                                           'required': '验证码不能为空'})


# 重置密码表单
class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6,
                               error_messages={'required': '密码不能为空',
                                               'min_length': '密码最小长度为6'})
    password2 = forms.CharField(required=True, min_length=6,
                                error_messages={'required': '密码不能为空',
                                                'min_length': '密码最小长度为6'})


# 用户修改头像表单
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['image']


# 用户修改个人信息表单
class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['username', 'birthday', 'gender', 'address', 'mobile_num']
