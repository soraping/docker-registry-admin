# Generated by Django 4.2 on 2023-07-25 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DockerImageRepositoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('name', models.CharField(max_length=20, verbose_name='项目名')),
            ],
            options={
                'verbose_name': '私服项目',
                'db_table': 'tianji_registry_repository',
            },
        ),
        migrations.CreateModel(
            name='DockerImageTagsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='镜像名')),
                ('tag', models.CharField(max_length=20, null=True, verbose_name='镜像tag')),
                ('digest', models.CharField(max_length=100, null=True, verbose_name='镜像摘要')),
                ('repository', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tag对应的镜像仓库名', to='docker_registry.dockerimagerepositorymodel')),
            ],
            options={
                'verbose_name': '私服镜像',
                'db_table': 'tianji_registry_images',
            },
        ),
    ]
