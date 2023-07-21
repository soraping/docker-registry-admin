from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'dcoker_registry/images-list.html')


class RegistryView(View):

    def post(self, request):
        return JsonResponse({
            'msg': 'hello'
        })