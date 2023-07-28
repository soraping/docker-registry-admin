import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class InterceptorMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response


    def process_request(self, request):
        print(request)

    def process_response(self, request, response):
        result = response.content.decode('utf-8')
        # logger.info(result)
        return response