from django.db import models
from tianji.models import BaseModel
from config import env


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
        db_table = env.TABLE_PREFIX + "projects"
        verbose_name = "项目表"


class ProjectHostModel(BaseModel):

    real_ip = models.CharField(
        max_length=40,
        verbose_name="物理IP"
    )

    virtual_ip = models.CharField(
        max_length=40,
        verbose_name="虚拟IP"
    )

    project = models.ForeignKey(
        "ProjectModel",
        on_delete=models.CASCADE,
        related_name="hosts"
    )

    tag = models.CharField(
        max_length=20,
        null=True,
        verbose_name="当前负载运行的镜像tag"
    )

    HOST_STATUS_CHOICES = (
        (0, "暂停中"),
        (1, "运行中"),
        (2, "已删除")
    )
    status = models.IntegerField(
        choices=HOST_STATUS_CHOICES,
        default=0,
        verbose_name="负载状态：0-暂停中，1-运行中，2-已删除",
        help_text="负载状态：0-暂停中，1-运行中，2-已删除"
    )

    class Meta:
        db_table = env.TABLE_PREFIX + "hosts"
        verbose_name = "项目负载IP"