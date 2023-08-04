from django.core.paginator import Paginator
from django.http import HttpRequest
from tianji.projects import models, forms
from utils import ErrorEnum, R
from constant import constants
import ujson
from django.forms.models import model_to_dict
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
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 数据类型转换
        dict_data = ujson.loads(json_data)
        # 参数为空判断
        if not dict_data.get('name'):
            return R.failed(ErrorEnum.PARAMS_IS_NULL)
    except Exception as e:
        logger.error("添加失败：{}".format(e))
        return R.failed(ErrorEnum.PARAMS_IS_ERROR)

    project_form = forms.ProjectForm(dict_data)
    if project_form.is_valid():
        project_form.save()
        return R.success()
    return R.failed(ErrorEnum.PARAMS_IS_ERROR)


def project_upd(request):
    try:
        json_data = request.body.decode()
        dict_data = ujson.loads(json_data)
        if not dict_data.get('id'):
            return R.failed(ErrorEnum.PARAMS_IS_NULL)
    except Exception as e:
        logger.error("更新失败：{}".format(e))
        return R.failed(ErrorEnum.PARAMS_IS_ERROR)

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
    project_name = request.GET.get('project_name')
    hosts = models.ProjectHostModel.objects.all()
    return R.success()


def add_host(request):
    """
    新增负载
    """
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 数据类型转换
        dict_data = ujson.loads(json_data)
        # 参数为空判断
        if not dict_data.get('project_id'):
            return R.failed(ErrorEnum.PARAMS_IS_NULL)
    except Exception as e:
        logger.error("添加负载失败：{}".format(e))
        return R.failed(ErrorEnum.PARAMS_IS_ERROR)

    hosts_form = forms.ProjectHostForm(dict_data)
    if hosts_form.is_valid():
        models.ProjectHostModel.objects.create(project_id=hosts_form.project_id,
                                               real_ip=hosts_form.real_ip, virtual_ip=hosts_form.virtual_ip)
    return R.failed(ErrorEnum.PARAMS_IS_ERROR)


def upd_host(request):
    """
    修改负载信息
    """
    pass
