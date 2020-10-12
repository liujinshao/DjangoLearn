from django.shortcuts import render,redirect,reverse
from .models import AxxUser,AxxUserInfo,ScoreConf,UserScore
# Create your views here.
from django_aixx.decorators import *
from resource.sign import sign, verify
from django.db.models import Sum
import string
import random
from django.core.mail import EmailMessage
from datetime import datetime


def register(request):
    if request.method=="GET":

        return render(request,"register.html")

    if request.method=="POST":
        from aixxuser.methods import md5
        param=request.POST.dict()
        param['password']=md5(param.get("password"))
        print(param)
        phone=AxxUser.objects.filter(phone=param.get("phone")).first()
        if phone:
            phone_msg="账号已存在"
            return render(request,"register.html",{"phone_msg":phone_msg,"phone":param.get("phone"),"email":param.get("email")})
        email=AxxUser.objects.filter(email=param.get("email")).first()
        if email:
            email_msg="邮箱已存在"
            return render(request, "register.html", {"email_msg": email_msg,"phone":param.get("phone"),"email":param.get("email")})
        # print(phone,email)
        param["status"]=False
        print(param)
        user=AxxUser.objects.create(**param)
        print(user)
        pk=user.pk
        print(pk)
        return redirect(to=reverse("next_reg",args=(pk,)))

def next_reg(request,pk):
    if request.method == "GET":

        return render(request, "next_base.html",{"pk":pk})
    if request.method=="POST":
        param=request.POST.dict()
        print(param)
        param["axxuser_id"]=pk
        file=request.FILES.get("photo")
        param["photo"]=file
        info=AxxUserInfo.objects.create(**param)
        print(info)
        user=info.axxuser
        user.status=True
        print(user)
        user.save()
        # 4. 赠送积分
        return redirect(to="/user/success?rn={}&n={}".format(info.realname, pk))
    return render(request, "next_base.html",{"pk":pk})

def success(request):

    realname=request.GET.get("rn")
    num=request.GET.get("n")
    # 通过 用户注册 动作，去 积分配置表，查询 是否赠送积分
    action = "用户注册"
    conf = ScoreConf.objects.get(action=action, status=True)
    # print(conf,"111")
    if conf is not None:
    #     # 获取赠送多少积分
        score_num = conf.score
        UserScore.objects.create(remark=action, score=score_num, user_id=num)

    return render(request, "success.html",{"realname":realname,"user":num})



def user_login(request):
    if request.method=="POST":
        phone=request.POST.get("name")
        pwd=request.POST.get("password")
        # print(phone,pwd)
        # 调用 authenticate 函数、验证权限
        phone=AxxUser.objects.filter(phone=phone).first()
        # print(phone)

        if phone is None:
            return render(request, "index.html", {"msg": "账号或密码不正确"})
        else:
            password = phone.password
            login_id = phone.id
            request.session.flush()         #先销毁之前session
            request.session.clear_expired()  # //查询前先清一次过期的
            request.session["login_id"]=login_id
            # print(request.session["login_id"])
            if password!=md5(pwd):

                return render(request, "index.html", {"msg": "账号或密码不正确"})

            # 如果账号密码正确、将登录标记存储到 会话 Session 中
            url=request.POST.get("url")
            if url:
                return redirect(url)
            return redirect(to="/")


@session_auth
def personal(request):
    login_id=request.session["login_id"]
    # print(login_id)
    score = UserScore.objects.filter(user_id=login_id).aggregate(score=Sum("score"))
    datas=AxxUserInfo.objects.get(axxuser_id=login_id)
    # print(datas,score)
    return render(request, "personal.html",{"data":datas,"score":score})

@session_auth
def bbs(request):


    return render(request,"bbs.html")

def form(request):
    from aixxuser.form import UserModelForm
    form = UserModelForm(data=request.POST)
    # print(form)
    if request.method=="GET":
        return render(request, "forms.html", {"data": form.as_table()})
    if request.method == "POST":
        if form.is_valid():
            param=form.cleaned_data
            print(param)
            return render(request, "forms.html", {"data": param})
        else:
            errors=form.errors
            print(errors)
            return render(request, "forms.html", {"errors": errors})

from django.views import View
class passwordSetView(View):

    def get(self,request):
        return render(request,"findpass.html")

    def post(self,request):

        phone=request.POST.get("phone")
        email=request.POST.get("email")
        print(phone,email)
        user=AxxUser.objects.filter(phone=phone).first()
        print(user.email)
        if user  is None:
            return JsonResponse({"status": False, "msg": "账号不存在"})
        if user.email!=email:
            return JsonResponse({"status": False, "msg": "输入的不是注册绑定的邮箱"})


        sex = "先生"
        if user.axxuser.sex == "f":
            sex = "女士"
        elif user.axxuser.sex == "s":
            sex = "先生/女士"
        find_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_password=''.join(random.choices(string.ascii_letters,k=6))
        print(find_time,new_password,sex,user.axxuser.realname)
        _param=_param = "password={}&pk={}&nice=liujin".format(new_password, user.pk)
        _sign=sign(_param)
        _href="{}://{}/user/active?{}&sign={}".format(request.scheme, request.get_host(), _param, _sign)

        body = """
                    <p>尊敬的{}{}, 您于{}在网站中找回密码</p>
                    <p>您的新密码是<b style="color:red;">{}</b>、点击链接<a href="{}">激活账户</a></p>
                    <p>如果不是您本人操作、请忽略该邮件。</p>
                """.format(user.axxuser.realname, sex, find_time, new_password, _href)
        # message = EmailMessage(subject="【爱下载】-密码找回", body=body, to=(email,))
        # # 设置 支持 html格式的 文本
        # message.content_subtype = "html"    #同步
        # # 发送邮箱
        # message.send()

        from aixxuser.tasks import send_mail
        send_mail.delay(body, to=(email,), subject="【爱下载】-密码找回", )
        # 响应一个结果
        return JsonResponse({"status": True, "msg": "邮件已发送、请及时查看邮件"})
from aixxuser.methods import *
class ActivePasswordView(View):
    def get(self,request):

        # 获取 新密码
        new_password = request.GET.get("password")

        # 获取 pk
        pk = request.GET.get("pk")
        # 获取 nice
        nice=request.GET.get("nice")
        print(new_password,pk,nice)
        # 获取签名
        _sign_text = request.GET.get("sign")
        _param = "password={}&pk={}&nice={}".format(new_password, pk, nice)
        print(new_password, pk, nice,_param)
        # return redirect(to="/")
        if verify(_param, _sign_text):
            user=AxxUser.objects.get(id=pk)
            user.password=md5(new_password)
            user.save()
            request.session.setdefault("msg", "密码已重置")
            return redirect(to="/")

def changepwd(request):
    if request.method=="GET":
        return render(request,"changepwd.html")
    if request.method == "POST":
        id = request.session["login_id"]
        password=request.POST.get("password")
        user=AxxUser.objects.get(id=id)
        user.password=md5(password)
        user.save()
        request.session.flush()
        request.session["msg"]="密码已修改，请重新登录"
        return redirect('/')
def checkpwd(request):
    pwd_old = md5(request.POST.get("pwd_old"))
    id = request.session["login_id"]
    user = AxxUser.objects.get(id=id)
    print(user.password)
    if user.password !=pwd_old:
        return JsonResponse({"msg":"旧密码不正确","proof":False},)
    return JsonResponse({"msg":"","proof":True})