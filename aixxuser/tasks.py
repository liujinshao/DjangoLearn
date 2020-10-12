from django_aixx.celerys import celery_app as app
from django.core.mail import EmailMessage


@app.task
def sum(a, b):
    return a+b


@app.task
def send_mail(body, to, subject):
    message = EmailMessage( body=body, to=to,subject=subject,)
    # 设置 支持 html格式的 文本
    message.content_subtype = "html"
    # 发送邮箱
    message.send()
