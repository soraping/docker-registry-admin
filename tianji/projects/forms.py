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

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['desc'].required = False
        self.fields['create_user'].required = False
        self.fields['update_user'].required = False


class ProjectHostForm(forms.Form):
    real_ip = forms.CharField()
    virtual_ip = forms.CharField()
    project_id = forms.IntegerField(
        required=True,
        error_messages={
            "required": "项目编号不能为空"
        }
    )


