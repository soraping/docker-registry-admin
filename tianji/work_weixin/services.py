import re
import logging
import requests
import ujson
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from constant import constants
from utils import R, ErrorEnum

from config import env
from tianji.work_weixin import models

logger = logging.getLogger(__name__)


def get_setting_list(request):
    page_no = int(request.GET.get('pageNo', constants.PAGE_NO))
    page_size = int(request.GET.get('pageSize', constants.PAGE_SIZE))

    query_set = models.WorkWeixin.objects.filter(is_delete=0).order_by("id")
    paginator = Paginator(query_set, page_size)

    page_total = paginator.count
    pro_list = paginator.page(page_no)
    data_list = [model_to_dict(data) for data in pro_list.object_list]
    return R.page(data=data_list, page_no=page_no, page_size=page_size, page_total=page_total)


def add_setting(request):
    pass


def upd_setting(request):
    pass


def send_msg_by_group(data):
    pass


def send_msg_by_robots(data):
    """
    机器人推送消息
    """
    event = data.get('event', {})
    message_name = event.get('message')
    app_key = event.get('key')
    origin_context = event.get('origin_context')
    if origin_context:
        match_obj = re.match(r'.*graylog_0:(.*)', origin_context)
        message_id = match_obj.group(1)
        redirect_url = f'{env.GRAY_LOG_DOMAIN}/messages/graylog_0/{message_id}'

        # 只推送机器人
        logger.info(f"触发机器人消息推送 url => {redirect_url}")
        work_weixin_setting = models.WorkWeixin.objects.filter(app_type=1, app_key=app_key).first()
        if work_weixin_setting:
            work_weixin_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={work_weixin_setting.webhook_key}'
            message_data = {
                "msgtype": "text",
                "text": {
                    "content": f"{message_name} 发生错误 具体信息点击地址查看 => \n {redirect_url}",
                    "mentioned_list": work_weixin_setting.user_ids.split(",")
                }
            }
            headers = {
                "Content-Type": "application/json"
            }
            work_weixin_result = requests.post(work_weixin_url, data=ujson.dumps(message_data), headers=headers)
