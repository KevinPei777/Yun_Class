from django import forms
import re

from Operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['user_name', 'mobile_nums', 'course_name']

    def clean_mobile_nums(self):
        # 验证手机号码
        mobile = self.cleaned_data['mobile_nums']
        regix_mobile = "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$"
        match_mobile = re.compile(regix_mobile)
        if match_mobile.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('请输入正确的手机号', code='invalid_mobile')
