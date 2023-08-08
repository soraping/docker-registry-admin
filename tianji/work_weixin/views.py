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
