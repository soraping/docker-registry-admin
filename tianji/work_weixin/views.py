from django.shortcuts import render
from django.views import View
from tianji.work_weixin import services


# Create your views here.

class WorkWeixinSettingView(View):

    def get(self, request):
        return render(request, "work_weixin/list.html")


class WorkWeixinSettingListView(View):

    def get(self, request):
        return services.get_setting_list(request)


class WorkWeixinAddView(View):

    def post(self, request):
        return services.add_setting(request)


class WorkWeixinUpdView(View):
    def post(self, request):
        return services.upd_setting(request)