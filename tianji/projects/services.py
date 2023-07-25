from django.core.paginator import Paginator
from django.http import HttpRequest
from tianji.projects import models
from utils import ErrorEnum, R
from constant import constants


def project_list(request: HttpRequest):
    page_no = int(request.GET.get('pageNo', constants.PAGE_NO))
    page_size = int(request.GET.get('pageSize', constants.PAGE_NO))

    query = models.ProjectModel.objects.filter(is_delete=False)
    search_name = request.GET.get('name')
    if search_name:
        query = query.filter(name__contains=search_name)

    query = query.order_by("id")
    paginator = Paginator(query, page_size)

    page_total = paginator.count
    pro_list =paginator.page(page_no)

    return R.page(data=pro_list, page_no=page_no, page_size=page_size, page_total=page_total)



