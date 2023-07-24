from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import ujson
from pprint import pprint


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'dcoker_registry/images-list.html')


class RegistryView(View):

    def post(self, request):
        result_str = request.body.decode('utf-8')
        result_json = ujson.loads(result_str)
        events = result_json['events']
        images = [
            dict(name=image['target']['repository'], tag=image['target']['tag'], digest=image['target']['digest'])
            for image in events
        ]
        pprint(images)

        return JsonResponse({
            'msg': 'success',
            'data': images
        })