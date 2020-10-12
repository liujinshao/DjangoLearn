from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from aixxuser.models import AxxUser,AxxUserInfo

# Create your models here.

class Resource(models.Model):
    resource = models.FileField(verbose_name="资源", upload_to="resource")
    resource_name = models.CharField(max_length=100, verbose_name="资源名称")
    keywords = models.CharField(max_length=200, verbose_name="关键字", help_text="关键字以空格进行分割")
    score = models.IntegerField(verbose_name="资源积分")
    resource_desc = models.TextField(verbose_name="资源描述", null=True, blank=True)
    ext = models.CharField(verbose_name="资源后缀", max_length=50, blank=True, null=True)
    size = models.IntegerField(verbose_name="资源大小", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="资源上传时间", default=timezone.now)

    # 定义一个关系属性 user
    user = models.ForeignKey(to=AxxUser, on_delete=models.DO_NOTHING, blank=True, related_name="resources")

    class Meta:
        managed=True
        db_table = "t_resource"


class DownloadResource(models.Model):
    download_user = models.ForeignKey(to=AxxUser, on_delete=models.DO_NOTHING, blank=True, related_name="downloads")
    resource = models.ForeignKey(to=Resource, on_delete=models.DO_NOTHING, blank=True, related_name="downloads")
    download_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "t_resource_download"

class CommentResource(models.Model):
    content = models.TextField(verbose_name="评论的内容")
    star = models.IntegerField(verbose_name="评论的星级", default=1)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    resource = models.ForeignKey(to=Resource, on_delete=models.DO_NOTHING, blank=True, related_name="comments")
    user = models.ForeignKey(to=AxxUser, on_delete=models.DO_NOTHING, blank=True, related_name="comments")
    class Meta:
        db_table = "t_resource_comment"


class Favorite(models.Model):
    resource = models.ForeignKey(to=Resource, on_delete=models.DO_NOTHING, blank=True, related_name="favorite")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    user=models.ForeignKey(to=AxxUser,related_name="favorite",on_delete=models.DO_NOTHING,blank=True)
    proof=models.CharField(max_length=10, verbose_name="收藏的凭据",blank=True,null=True)
    class Meta:

        db_table="t_favorite"

class StarConf(models.Model):
    star=models.IntegerField(primary_key=True,verbose_name="星级")
    num=models.IntegerField(verbose_name="评论数")

    class Meta:

        db_table="t_star_conf"