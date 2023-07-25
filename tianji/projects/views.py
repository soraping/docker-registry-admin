from django.shortcuts import render
from django.views import View
from tianji.projects import services


# Create your views here.
class ProjectView(View):

    def get(self, request):
        return render(request, 'projects/list.html')


class ProjectListView(View):
    """
    查询项目列表
    """

    def get(self, request):
        result = services.project_list(request)
        return result


class ProjectAddView(View):

    def post(self, request):
        return services.project_add(request)

