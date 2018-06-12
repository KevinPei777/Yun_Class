from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from Munet1.settings import EMAIL_FROM
import random, string


def send_register_email(email, send_type):
    email_record = EmailVerifyRecord()
    # 生成随即字符串验证码
    if send_type == 'update_email':
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    else:
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
    email_record.verify_code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = "在线云课堂注册激活链接"
        email_body = '请点击下列链接激活您的帐号:\nhttp://127.0.0.1:8000/active/{0}'\
            .format(email_record.verify_code)
        send_status = send_mail(email_title, email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = "在线云课堂重置密码链接"
        email_body = '请点击下列链接重置您的密码:\nhttp://127.0.0.1:8000/reset/{0}' \
            .format(email_record.verify_code)
        send_status = send_mail(email_title, email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = '在线云课堂修改邮箱信息'
        email_body = '您的验证码为:\n{0}'.format(email_record.verify_code)
        send_status = send_mail(email_title, email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if send_status:
            pass
