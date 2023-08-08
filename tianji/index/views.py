from django.shortcuts import render
from django.views import View
import ujson
from pprint import pprint
from utils import R
from tianji.work_weixin import services as weixin


# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class CallbackView(View):
    def post(self, request, msg_channel):
        result_str = request.body.decode('utf-8')
        result_json = ujson.loads(result_str)
        pprint(result_json)
        if msg_channel == "work_weixin":
            weixin.send_msg_by_robots(result_json)
        return R.success()