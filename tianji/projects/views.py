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


class ProjectUpdateView(View):

    def post(self, request):
        return services.project_upd(request)


class ProjectDetailView(View):

    def get(self, request):
        return services.project_detail(request)


class ProjectHostView(View):
    def get(self, request):
        # 获取页面传递参数
        project_name = request.GET.get('project_name')
        project_id = request.GET.get('project_id')
        return render(request, 'projects/host.html', {"project_name": project_name, 'project_id': project_id})


class ProjectHostListView(View):

    def get(self, request):
        return services.project_host_list(request)


class ProjectHostAddView(View):
    def post(self, request):
        return services.add_host(request)


class ProjectHostUpdView(View):
    def post(self, request):
        return services.upd_host(request)