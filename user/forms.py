 # 通过django.forms定义表单
from django import forms
from . import models


class RegisterForm(forms.Form):
    """注册表单"""
    # 因为Model中的元素默认是会把密码显示出来的，所以在这里重新定义一个password
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)

    @property
    def clean_username(self):
        """
        对username字段做检查用户名是否已经被注册
        注意字段一定要有返回值
        """
        # self.cleaned_data["username"] => 获取表单提交的username数据
        users = models.User.objects.filter(username=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        else:
            raise forms.ValidationError("该用户名已经被使用")




class LoginForm(forms.Form):
    """登录表单"""
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    def clean(self):
        user = models.User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not user:
            raise forms.ValidationError("用户不存在")
        else:
            self.cleaned_data["user"]=user
            return self.cleaned_data