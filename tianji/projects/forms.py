from django import forms
from tianji.projects import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.ProjectModel
        fields = '__all__'
        error_messages = {
            'name': {
                'required': "项目名不能为空",
                'invalid': "请输入一个正确的项目名"
            }
        }
