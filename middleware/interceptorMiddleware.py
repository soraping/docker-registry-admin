import logging
import ujson
from django.http import HttpRequest
from utils import R, ErrorEnum

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class InterceptorMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request: HttpRequest):
        if request.method == 'POST':
            try:
                json_data = request.body.decode('utf-8')
                dict_data = ujson.loads(json_data)
                request.POST = dict_data
            except Exception as e:
                return R.failed(ErrorEnum.PARAMS_IS_ERROR)

    def process_response(self, request, response):
        result = response.content.decode('utf-8')
        # logger.info(result)
        return response