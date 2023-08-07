from django.db import models
from tianji.models import BaseModel
from config import env


# Create your models here.

class WorkWeixin(BaseModel):
    app_name = models.CharField(
        max_length=20,
        verbose_name="应用名称"
    )

    corpid = models.CharField(
        max_length=18,
        verbose_name="企业微信appid"
    )

    APP_TYPE_CHOICES = (
        (1, "机器人推送"),
        (2, "群消息推送")
    )

    app_type = models.IntegerField(
        choices=APP_TYPE_CHOICES,
        default=1,
        verbose_name="应用类型"
    )

    corpsecret = models.CharField(
        null=True,
        max_length=200,
        verbose_name="应用secret"
    )

    webhook_key = models.CharField(
        null=True,
        max_length=200,
        verbose_name="机器人应用key"
    )

    chat_name = models.CharField(
        null=True,
        max_length=20,
        verbose_name="群名称"
    )

    chat_id = models.CharField(
        null=True,
        max_length=20,
        verbose_name="群ID"
    )

    user_ids = models.CharField(
        null=True,
        max_length=200,
        verbose_name="群成员/消息推送目标"
    )

    class Meta:
        db_table = env.TABLE_PREFIX + "work_weixin"
        verbose_name = "企业微信的一些参数"
