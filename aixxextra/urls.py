from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path("stu",views.StudentListView.as_view()),
    path("attention",views.attention,name="attention"),
    path("student/<pk>",views.student,name="student"),
    path("aaaaaa",views.aaaaaa,name="aaaaaa"),
    path("zfb_recharge",views.zfb_recharge,name="zfb_recharge"),
    path("zfb_recharge_success",views.zfb_recharge_success,name="zfb_recharge_success"),

]
