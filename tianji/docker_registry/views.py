from django.shortcuts import render
from django.views import View
import ujson
from tianji.docker_registry import services


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'dcoker_registry/images-list.html')


class RegistryView(View):

    def post(self, request):
        result_str = request.body.decode('utf-8')
        result_json = ujson.loads(result_str)
        events = result_json['events']
        return services.registry_tag_push(events)