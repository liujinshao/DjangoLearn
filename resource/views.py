from django.shortcuts import render,redirect
from resource.models import Resource,DownloadResource,CommentResource,Favorite,StarConf
from aixxuser.models import AxxUser,AxxUserInfo,ScoreConf,UserScore
from django.http import HttpResponse,response,JsonResponse
from django.http import StreamingHttpResponse  # # 设置响应头 StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
from django.core.paginator import Paginator
from django.db.models import Sum
from aixxextra.models import Attention
import os
# Create your views here.
from django_aixx.decorators import *
@session_auth
def upload(request):
    if request.method=="GET":

        return  render(request,"upload.html")
    if request.method=="POST":
        login_id=request.session["login_id"]
        param=request.POST.dict()
        res=request.FILES.get("resource")
        ext=str(res).split(".")[1]
        size=res.size
        param["resource"]=res
        param['ext']=ext
        param["size"]=size
        param["user_id"]=login_id
        print(param,login_id)
        Resource.objects.create(**param)
        action = "上传"
        conf = ScoreConf.objects.get(action=action, status=True)
        if conf is not None:
            #     # 获取赠送多少积分
            score_num = conf.score
            UserScore.objects.create(remark=action, score=score_num, user_id=login_id)
        return redirect(to='/')

def detail(request,pk):  #pk当前资源的id

    resource=Resource.objects.get(id=pk)       #获取当前资源模型对象

    comments=CommentResource.objects.filter(resource_id=pk).order_by("-create_time")  #获取评论模型对象并用时间降序
    s_num=1
    for num in range(5,0,-1):
        star = CommentResource.objects.filter(resource_id=pk,star__gte=num).count()  # 获取当前资源所有评论
        star_num=StarConf.objects.get(star=num).num
        # print(star,star_num)
        if star>=star_num:
            s_num=num
            break
    # print(s_num,resource.downloads.count())
    msg2 = "关注"
    try:
        login_id = request.session["login_id"]  # 获取当前登录用户id
        att = Attention.objects.filter(user_id=login_id, usered_id=resource.user_id) #获取关注表对应关注信息的模型对象
        print(len(att), )
        if len(att) == 1:
            msg2 = "已关注"
    except:
        print("未登录，详情")
    try:
        login_id = request.session["login_id"]  # 获取当前登录用户id
        proof = Favorite.objects.filter(user_id=login_id, resource_id=pk).first().proof  #获取收藏证明

        msg="收藏"
        if proof == "1":
            msg = "已收藏"
        return render(request, "detail.html", {"resource": resource, "comments": comments,"msg":msg,"msg2":msg2,"num":s_num})
    except:
         msg="收藏"
         return render(request, "detail.html", {"resource": resource, "comments": comments,"msg":msg,"msg2":msg2,"num":s_num})


@session_auth
def shoucang(request):
    if request.method=="GET":
        login_id=request.session["login_id"]
        favorite=Favorite.objects.filter(user_id=login_id).order_by("-create_time")
        # 创建一个 分页器、进行数据的分页
        paginator = Paginator(favorite, 4)

        # 从浏览器获取 页码
        number = request.GET.get("page", 1)

        # 根据页码 获取指定的数据
        page = paginator.get_page(number)
        return render(request, "shoucang.html",{"data":page})
@session_auth
def favorite(request):
    param = request.POST.dict()
    user_id = request.session["login_id"]
    # print(param["resource_id"])
    try:
        proof = Favorite.objects.filter(user_id=user_id,resource_id=param["resource_id"]).first().proof #获取资源证明
        if proof=="1":
            print("删除收藏")
            Favorite.objects.filter(user_id=user_id,resource_id=param["resource_id"]).delete()
            return JsonResponse({"msg":"收藏"})
    except:
        print("执行收藏")
        param["user_id"] = user_id
        param["proof"] = 1
        Favorite.objects.create(**param)
        return JsonResponse({"msg": "已收藏"})

@session_auth
def point(request):
    if request.method=="POST":
        #查询用户积分，并根据remark分组计算
        data=UserScore.objects.filter(user_id=request.session["login_id"]).values("remark").annotate(value=Sum("score"))
        print("data")
        data=list(data)
        return JsonResponse(data=data,safe=False)
    return render(request, "point.html")

def userpoint(request):
    # 查询近一周的用户注册信息
    from datetime import datetime, timedelta

    # 获取 指定时间的所有注册信息
    queryset = AxxUserInfo.objects.filter(date_joined__date__gte=datetime.now() - timedelta(days=6))

    # 当当天的注册信息、按小时 进行分组
    from django.db.models import Func, F, Count
    from django.db.models.functions import TruncDate

    queryset = queryset.annotate(hour=Func(F("date_joined"), function="hour"),
                                 day=TruncDate("date_joined")).values("hour", "day").annotate(
        num=Count("hour"))

    # 将 queryset 转成 列表
    data = list(queryset)
    print(data)
    return JsonResponse(data=data, safe=False)
@session_auth
def download(request,pk):
    # print("资源pk",pk)
    data=Resource.objects.get(id=pk)               #得到resource模型对象
    name=data.resource
    filename=str(name).split("/")[-1]             #切割出文件名
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #项目根目录
    file_path = os.path.join(base_dir,"media",str(name) )                # 下载文件的绝对路径
    # print(name,filename,base_dir,file_path)


    if not os.path.isfile(file_path):  # 判断下载文件是否存在
        return HttpResponse("Sorry but Not Found the File")
    def file_iterator(file_path, chunk_size=512):
        with open(file_path,mode="rb")as f:
            while True:
                c=f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    action1 = "资源被下载"
    action2 = "下载资源"
    add_score=data.score
    minus_score=0-add_score
    add_id=data.user_id                      #资源上传者id
    resource_id=data.id                      #资源在资源表的id
    minus_id=request.session["login_id"]     #当前登录者的id  也是下载者id
    # print(add_score, add_id, minus_id)
    response = StreamingHttpResponse(file_iterator(file_path))
    # 以流的形式下载文件,这样可以实现任意格式的文件下载
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + urlquote(filename)  # 解决中文乱码
    if add_id==minus_id:    #下载自己的资源不记录
        return response

    DownloadResource.objects.create(download_user_id=minus_id,resource_id=resource_id)  #生成日志记录
    UserScore.objects.create(remark=action1, score=add_score, user_id=add_id)           #给被下载用户加积分
    UserScore.objects.create(remark=action2, score=minus_score, user_id=minus_id)       #下载用户减积分
    return response
def download_check(request,pk):
    print("校验页面")
    data={"a":"aa"}
    return JsonResponse(data)
@session_auth
def comment(request):
    comment_id=request.session["login_id"]        #获得评论人id
    print("评论人id",comment_id)
    param=request.POST.dict()                  #获取异步请求数据
    param["user_id"]=comment_id
    res_user_id=Resource.objects.get(id=param.get("resource_id")).user_id
    if res_user_id!=comment_id:

        comment_db=CommentResource.objects.create(**param)    #将数据插入到数据库
        from django.forms.models import model_to_dict
        result = AxxUserInfo.objects.filter(axxuser_id=comment_id).values("nickname","photo").first()
        print(result)
        #
        # comment["nickname"] = nickname
        comment=model_to_dict(comment_db)                               #转成字典  注意  此刻不在是模型对象了
        comment["create_time"] = comment_db.create_time
        comment.update(result)                                  #字典update方法把字典2的内容加到字典一
        # print(comment)
        action = "评论"
        conf = ScoreConf.objects.get(action=action, status=True)
        # print(conf,"111")
        if conf is not None:
            #     # 获取赠送多少积分
            score_num = conf.score
            UserScore.objects.create(remark=action, score=score_num, user_id=comment_id)
        return JsonResponse(comment)
    return JsonResponse({"msg":"不能评论自己上传的文件！！！！"})


