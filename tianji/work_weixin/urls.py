from django.urls import path
from tianji.work_weixin import views

urlpatterns = [
    path("", views.WorkWeixinSettingView.as_view(), name='work_weixin_setting_page'),
    path('list', views.WorkWeixinSettingListView.as_view())
]