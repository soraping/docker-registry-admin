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