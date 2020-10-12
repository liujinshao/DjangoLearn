from django.views.generic import ListView,UpdateView,DeleteView
from django.shortcuts import render,reverse
from django.views import View
from aixxuser.form import UserModelForm
from resource.models import Resource
from aixxuser.models import AxxUserInfo
from django.shortcuts import redirect
from django.http import JsonResponse,HttpResponse
# class StudentView(View):
#
#     def get(self, request, *args, **kwargs):
#         form = UserModelForm()
#         return render(request, "student/students.html", {"form": form.as_p()})
#
#     def post(self, request, *args, **kwargs):
#         # 接收页面参数、并校验
#         form = UserModelForm(data=request.POST)
#
#         if form.is_valid():
#             # 保存数据
#             form.save()
#
#             return redirect(to="/user/stu/index")
#         return render(request, "student/students.html", {"form": form.as_p()})
# Create your views here.
class StudentListView(ListView):     #全局搜索；list.py  在里面可看
    model=AxxUserInfo

    template_name="student/students.html"

    def get(self, request, *args, **kwargs):  # 重写get方法
        response = super().get(request, *args, **kwargs)
        return response

class StudentUpdateView(UpdateView):

    queryset = AxxUserInfo.objects.all()
    # model =            #二选其一


from aixxextra.models import Attention
def attention(request):
    if request.method=="GET":
        attention=Attention.objects.filter(user_id=request.session["login_id"])

        return render(request,"attention.html",{"attention":attention})
    if request.method == "POST":
        login_id=request.session['login_id']
        resource_user_id=request.POST.get("resource_user_id")
        # print(login_id,login_id)
        try:
            proof=Attention.objects.filter(user_id=login_id,usered_id=resource_user_id).first()
            # print(proof)
            if proof.user_id==login_id :
                Attention.objects.filter(user_id=login_id,usered_id=resource_user_id).delete()
                return JsonResponse({"msg2":"关注"})
        except:
            Attention.objects.create(user_id=login_id,usered_id=resource_user_id)

            return JsonResponse({"msg2":"已关注"})


def aaaaaa(request):
    print("进来了")
    a={"a":1}
    b=2
    return redirect(to=reverse('student',kwargs={"pk":"{'name':'qike','pwd':123456,'aa':'aaa'}"}))

def student(request,pk):

    print(pk,type(pk))

    return render(request,"student/students.html")

def zfb_recharge(request):
    # 获取充值的金额
    money = request.GET.get("m")

    from django_aixx.alipayUtils import alipay_client
    # 创建一个 接口模型对象、用来接收参数
    # alipay.trade.page.pay
    from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
    # 生成一个订单号
    import uuid

    out_trade_no = uuid.uuid4().hex
    model = AlipayTradePagePayModel()
    model.out_trade_no = out_trade_no
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    model.total_amount = money
    model.subject = "爱下载-积分充值"
    # 创建一个 支付宝支付的 请求对象
    from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
    alipay_request = AlipayTradePagePayRequest(biz_model=model)

    # 配置支付成功后的 回调地址
    alipay_request.return_url = "http://192.168.0.91:8888/extra/zfb_recharge_success"

    # 通过 client 对象、执行 请求 对象、并返回响应的内容
    response_content = alipay_client().page_execute(alipay_request)

    return HttpResponse(response_content)
def zfb_recharge_success(request):
    # 接收支付宝支付成功后的发送的参数

    # 获取商户订单号
    out_trade_no = request.GET.get("out_trade_no")

    # 获取交易金额
    total_amount = request.GET.get("total_amount")

    from django_aixx.alipayUtils import alipay_client
    from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
    from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
    from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse

    # 获取查询接口对应的模型 alipay.trade.query
    model = AlipayTradeQueryModel()
    model.out_trade_no = out_trade_no

    # 获取执行 接口的请求对象
    alipay_request = AlipayTradeQueryRequest(biz_model=model)

    # 执行请求对象、并获取响应的结果
    response_content = alipay_client().execute(alipay_request)

    # 解析响应的结果
    response = AlipayTradeQueryResponse()

    response.parse_response_content(response_content)

    if response.is_success():

        # 支付成功的话、进行充值
        from aixxuser.models import UserScore, ScoreConf

        conf = ScoreConf.objects.filter(action="支付宝充值", status=True).first()
        if conf is not None:
            # 获取支付宝充值比例
            score_num = conf.score

            # 获取充值的积分
            score_jf = score_num * float(total_amount)

            UserScore.objects.create(remark="支付宝充值", score=score_jf, user_id=request.session["login_id"])

        return redirect(to="/user/personal")

    return redirect(to="/user/personal")

