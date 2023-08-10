from django import forms


class WorkWeixinForm(forms.Form):
    app_name = forms.CharField()
    app_key = forms.CharField()
    corpid = forms.CharField()
    app_type = forms.IntegerField()
    corpsecret = forms.CharField()
    chat_name = forms.CharField()
    user_ids = forms.CharField()
