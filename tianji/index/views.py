from django.shortcuts import render
from django.views import View
import ujson
from pprint import pprint
from utils import R
from tianji.work_weixin import services


# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class CallbackView(View):
    def post(self, request):
        """
        最终跳转地址
        http://118.192.66.57:5002/messages/graylog_0/f7ba9d81-358c-11ee-84c7-0242ac140004
        """
        result_str = request.body.decode('utf-8')
        result_json = ujson.loads(result_str)
        pprint(result_json)
        event = result_json.get('event', {})
        event_key = event.get('key')
        if event_key == 'mall':
            services.send_msg_by_robots(result_json)
        return R.success()