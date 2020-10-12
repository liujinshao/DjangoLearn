from django.db import models

# Create your models here.
class AxxUser(models.Model):
    phone = models.CharField(unique=True, max_length=11)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=50)
    status = models.IntegerField(blank=True, null=True)
    reg_time = models.DateTimeField(blank=True, null=True)
    alipay_user_id = models.CharField(max_length=100, blank=True, null=True)
    qq_user_id = models.CharField(max_length=100, blank=True, null=True)
    wx_user_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'axx_user'


class AxxUserInfo(models.Model):
    birth = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    realname = models.CharField(max_length=100, blank=True, null=True)
    _sex_choice=(
        ("f","女"),
        ("m","男"),
        ("s","保密")
    )

    sex = models.CharField(max_length=1, blank=True, null=True,)
    photo = models.FileField(upload_to='photo',null=True,blank=True)
    date_joined=models.DateTimeField(auto_now=True)
    axxuser = models.OneToOneField(to="AxxUser", related_name="axxuser", on_delete=models.CASCADE, blank=True)
    class Meta:
        managed = True
        db_table = 'axx_user_info'


# 积分配置
class ScoreConf(models.Model):
    action = models.CharField(max_length=100, verbose_name="执行的动作")
    score = models.IntegerField(verbose_name="赠送的积分数")
    status = models.BooleanField(verbose_name="是否开启功能", default=True)
    class Meta:
        managed=True
        db_table = "t_score_conf"


# 用户积分
class UserScore(models.Model):
    remark = models.CharField(max_length=100, verbose_name="积分来源")
    score = models.IntegerField(verbose_name="积分数")
    user = models.ForeignKey(to=AxxUser, on_delete=models.DO_NOTHING, blank=True, related_name="scores")
    create_time = models.DateTimeField(verbose_name="积分获取时间", auto_now_add=True)
    class Meta:
        managed = True
        db_table = "t_user_score"

class Logger(models.Model):
    username=models.CharField(max_length=100,verbose_name="访问的用户")
    func_name=models.CharField(max_length=100,verbose_name="功能名")
    func_args=models.CharField(max_length=100,verbose_name="参数1",blank=True,null=True)
    func_kwargs=models.CharField(max_length=200,verbose_name="参数2",blank=True,null=True)
    content=models.TextField(verbose_name="响应的结果",blank=True,null=True)
    error_code=models.CharField(max_length=100,verbose_name="异常编码",blank=True,null=True)
    error_msg=models.TextField(verbose_name="异常信息",blank=True,null=True)
    ip_address=models.CharField(max_length=300,verbose_name="客户端id")
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="访问时间")
    path=models.CharField(max_length=100,verbose_name="请求地址",blank=True,null=True)
    status=models.IntegerField(verbose_name="状态码",blank=True,null=True)
    class Meta:

        db_table="t_logger"
