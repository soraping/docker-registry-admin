from pprint import pprint
from utils import ErrorEnum, R
from tianji.docker_registry.models import DockerImageTagsModel


def registry_tag_push(events):
    """
    保存回调的镜像tag信息
    """
    images = [
        DockerImageTagsModel(name=image['target']['repository'], tag=image['target']['tag'], digest=image['target']['digest'])
        for image in events
        # 指定 push 事件
        if image['action'] == 'push'
    ]
    DockerImageTagsModel.objects.bulk_create(images)
    return R.success()


def registry_tag_list(image_name):
    """
    根据镜像名查询该镜像所有的记录tag
    """
    image_tag_list = DockerImageTagsModel.objects.filter(name=image_name).order_by('-pk')[:5]
    return R.success(data=list(image_tag_list))