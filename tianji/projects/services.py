from django.core.paginator import Paginator
from django.http import HttpRequest
from tianji.projects import models, forms
from utils import ErrorEnum, R
from constant import constants
from django.forms.models import model_to_dict
from django.db.models import  Q
import logging

logger = logging.getLogger(__name__)


def project_list(request: HttpRequest):
    page_no = int(request.GET.get('pageNo', constants.PAGE_NO))
    page_size = int(request.GET.get('pageSize', constants.PAGE_SIZE))

    query = models.ProjectModel \
        .objects.only('name', 'id', 'desc') \
        .filter(is_delete=False)
    search_name = request.GET.get('name')
    if search_name:
        query = query.filter(name__contains=search_name)

    query = query.order_by("id")
    paginator = Paginator(query, page_size)

    page_total = paginator.count
    pro_list = paginator.page(page_no)
    data_list = [model_to_dict(data) for data in pro_list.object_list]
    return R.page(data=data_list, page_no=page_no, page_size=page_size, page_total=page_total)


def project_add(request):
    """
    新增项目
    """
    post_data = request.POST
    project_form = forms.ProjectForm(post_data)
    if project_form.is_valid():
        project_form.save()
        return R.success()
    return R.failed(ErrorEnum.PARAMS_IS_ERROR)


def project_upd(request):

    dict_data = request.POST
    if not dict_data.get('id'):
        return R.failed(ErrorEnum.PARAMS_IS_NULL)
    models.ProjectModel.objects.filter(id=dict_data.get('id')) \
        .update(desc=dict_data.get('desc'), name=dict_data.get('name'))

    return R.success()


def project_detail(request):
    """
    查询项目所配置的负载信息
    """
    project_name = request.GET.get('name')
    if project_name:
        query_set = models.ProjectModel.objects.filter(name=project_name)
        project_detail = query_set.prefetch_related("projecthostmodel_set").all()
        return R.success(project_detail)
    else:
        return R.failed(ErrorEnum.PARAMS_IS_NULL)


def project_host_list(request):
    """
    负载列表
    """
    project_id = request.GET.get('project_id')

    # hosts_set = models.ProjectHostModel.objects.filter(project__id=project_id).filter(~Q(status=2))
    # 使用 related_name 反查
    project = models.ProjectModel.objects.get(id=project_id)
    hosts_set = project.hosts.filter(~Q(status=4))
    hosts = [
        {
            "id": host.id,
            "project_id": host.project_id,
            "real_ip": host.real_ip,
            'virtual_ip': host.virtual_ip,
            'tag': host.tag,
            # 待选择版本
            'select_tags': ['1.0', '1.1', '1.2'],
            'status': host.status
        }
        for host in list(hosts_set)
    ]
    return R.success(data=hosts)


def add_host(request):
    """
    新增负载
    """
    dict_data = request.POST
    hosts_form = forms.ProjectHostForm(dict_data)
    if hosts_form.is_valid():
        project_info = models.ProjectModel.objects.get(id=dict_data.get('project_id'))
        host = models.ProjectHostModel(project_id=project_info.id,
                                       real_ip=dict_data.get('real_ip'),
                                       virtual_ip=dict_data.get('virtual_ip'))
        host.save()
        return R.success()
    return R.failed(ErrorEnum.PARAMS_IS_ERROR)


def upd_host(request):
    """
    修改负载信息
    """
    pass


def change_tag(request):
    """
    切换版本
    """
    dict_data = request.POST
    if not dict_data.get('id') or not dict_data.get('tag') or not dict_data.get('project_id'):
        return R.failed(ErrorEnum.PARAMS_IS_NULL)

    # 需要切换的版本
    change_tag = dict_data.get('tag')
    project_id = dict_data.get('project_id')

    # 使用消息队列

    # 修改数据库信息
    # models.ProjectHostModel.objects.filter(id=dict_data.get('id')).update(tag=change_tag)

    return R.success()

def loop_tag_status(request):
    pass