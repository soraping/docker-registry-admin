# Generated by Django 4.2 on 2023-07-28 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_projectmodel_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='create_user',
            field=models.IntegerField(default=0, null=True, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='projectmodel',
            name='update_user',
            field=models.IntegerField(default=0, null=True, verbose_name='更新人'),
        ),
    ]