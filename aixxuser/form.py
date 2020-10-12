from django import forms
from django.forms import ModelForm
from aixxuser.models import AxxUserInfo,AxxUser
class BbsForm(forms.Form):

    name=forms.CharField(max_length=100,min_length=3,label="名字")
    password=forms.CharField(max_length=100,min_length=3,label="密码")
    resource=forms.FileField(label="资源")

class UserModelForm(ModelForm):
    class Meta:
        model = AxxUser
        # fields = ["bbs_type", "subject"]
        fields = "__all__"
