from django.http import JsonResponse
from utils.ErrorEnum import ErrorEnum
from constant import constants


def success(data):
    result = {
        'msg': constants.MESSAGE_SUCCESS,
        'data': data
    }
    return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False})


def page(data, page_no, page_size, page_total):
    result = {
        'dataList': data,
        'pageNo': page_no,
        'pageSize': page_size,
        'total': page_total
    }
    return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False})


def failed(error: ErrorEnum):
    result = {
        'code': error.code,
        'msg': error.msg
    }
    return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False})
