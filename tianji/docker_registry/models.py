from django.db import models
from tianji.models import BaseModel
from config import env


# Create your models here.

class DockerImages(BaseModel):

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

    class Meta:
        db_table = env.TABLE_PREFIX + "registry_images"
        verbose_name = "私服镜像"
