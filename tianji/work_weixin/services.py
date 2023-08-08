import re
import logging
import requests
import ujson

from config import env
from tianji.work_weixin import models

logger = logging.getLogger(__name__)


def send_msg_by_group(data):
    pass


def send_msg_by_robots(data):
    """
    机器人推送消息
    """
    event = data.get('event', {})
    app_name = event.get('message')
    origin_context = event.get('origin_context')
    if origin_context:
        match_obj = re.match(r'.*graylog_0:(.*)', origin_context)
        message_id = match_obj.group(1)
        redirect_url = f'{env.GRAY_LOG_DOMAIN}/messages/graylog_0/{message_id}'
        logger.info(f"触发机器人消息推送 url => {redirect_url}")
        work_weixins = models.WorkWeixin.objects.filter(app_type=1).first()
        work_weixin_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={work_weixins.webhook_key}'
        message_data = {
            "msgtype": "text",
            "text": {
                "content": f"{app_name} 发生错误 具体信息点击地址查看 => \n {redirect_url}",
                "mentioned_list": ['@all']
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        work_weixin_result = requests.post(work_weixin_url, data=ujson.dumps(message_data), headers=headers)
