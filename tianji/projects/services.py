from django.core.paginator import Paginator
from django.http import HttpRequest
from tianji.projects import models, forms
from utils import ErrorEnum, R
from constant import constants
import ujson
import logging


def project_list(request: HttpRequest):
    page_no = int(request.GET.get('pageNo', constants.PAGE_NO))
    page_size = int(request.GET.get('pageSize', constants.PAGE_SIZE))

    query = models.ProjectModel.objects.filter(is_delete=False)
    search_name = request.GET.get('name')
    if search_name:
        query = query.filter(name__contains=search_name)

    query = query.order_by("id")
    paginator = Paginator(query, page_size)

    page_total = paginator.count
    pro_list = paginator.page(page_no)

    return R.page(data=list(pro_list.object_list), page_no=page_no, page_size=page_size, page_total=page_total)


def project_add(request):
    """
    新增项目
    """
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed(ErrorEnum.PARAMS_IS_NULL)
        # 数据类型转换
        dict_data = ujson.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed(ErrorEnum.PARAMS_IS_ERROR)

    project_form = forms.ProjectForm(dict_data)
    if project_form.is_valid():
        project_form.save()
        return R.success()
    return R.failed(ErrorEnum.PARAMS_IS_ERROR)