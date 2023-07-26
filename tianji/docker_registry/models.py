from django.db import models
from tianji.models import BaseModel
from config import env


# Create your models here.
class DockerImageRepositoryModel(BaseModel):
    name = models.CharField(
        max_length=20,
        verbose_name="项目名"
    )

    class Meta:
        db_table = env.TABLE_PREFIX + "registry_repository"
        verbose_name = "私服项目"


class DockerImageTagsModel(BaseModel):
    name = models.CharField(
        null=True,
        max_length=100,
        verbose_name="镜像名"
    )

    tag = models.CharField(
        null=True,
        max_length=20,
        verbose_name="镜像tag"
    )

    digest = models.CharField(
        null=True,
        max_length=100,
        verbose_name="镜像摘要"
    )

    # repository = models.ForeignKey(
    #     "DockerImageRepositoryModel",
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     related_name='tag对应的镜像仓库名'
    # )

    class Meta:
        db_table = env.TABLE_PREFIX + "registry_images"
        verbose_name = "私服镜像"
