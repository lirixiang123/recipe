from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    """登录判断器"""
    def wrapper(request,*view_args,**view_kwargs):
        if request.user.is_authenticated:
            return view_func(request,*view_args,**view_kwargs)
        else:
            return redirect(reverse("user:login"))
    return wrapper
