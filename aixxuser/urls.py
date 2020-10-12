from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path("register",views.register,name="register"),
    path("next_reg/<pk>",views.next_reg,name="next_reg"),
    path("success",views.success,name="success"),
    path("user_login",views.user_login,name="user_login"),
    path("bbs",views.bbs,name="bbs"),
    path("form",views.form,name="form"),
    path('pwd',views.passwordSetView.as_view(),name="pwd_find"),
    path('active',views.ActivePasswordView.as_view(),name="pwd_active"),

    path("personal",views.personal,name="personal"),
    path("changepwd",views.changepwd,name="changepwd"),
    path("checkpwd",views.checkpwd,name="checkpwd"),
]
