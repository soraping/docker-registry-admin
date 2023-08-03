from django.db import models
from tianji.models import BaseModel


# Create your models here.
class ProjectModel(BaseModel):
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="项目名"
    )

    desc = models.TextField(
        null=True,
        max_length=150,
        verbose_name="项目使用描述"
    )

    class Meta:
        db_table = "projects"
        verbose_name = "项目表"


class ProjectHostModel(BaseModel):
    ip = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="主机IP"
    )

    project = models.ForeignKey(
        "ProjectModel",
        on_delete=models.CASCADE
    )

    tag = models.CharField(
        max_length=20,
        null=True,
        verbose_name="当前负载运行的镜像tag"
    )

    class Meta:
        db_table = "hosts"
        verbose_name = "项目负载IP"