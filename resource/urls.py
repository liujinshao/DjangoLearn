from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path("upload",views.upload,name="upload"),
    path("detail/<pk>", views.detail, name="detail"),
    path("shoucang", views.shoucang, name="shoucang"),
    path("point", views.point, name="point"),
    path("userpoint", views.userpoint, name="userpoint"),
    path("download/<pk>", views.download, name="download"),
    path('download/<int:pk>/check', views.download_check, name="check"),
    path('comment', views.comment, name="comment"),
    path('favorite', views.favorite, name="favorite"),
]
