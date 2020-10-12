from django.db import models
from aixxuser.models import AxxUser,AxxUserInfo
# Create your models here.

class Attention(models.Model):
    user=models.ForeignKey(to=AxxUser,related_name="useratt",on_delete=models.DO_NOTHING,verbose_name="收藏者id")
    usered=models.ForeignKey(to=AxxUser,related_name="useredatt",on_delete=models.DO_NOTHING,verbose_name="被收藏者id")

    class Meta:
        db_table="t_attention"
