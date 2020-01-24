from django.shortcuts import render, redirect
from .forms import  RegisterForm, LoginForm
from .models import User

# Create your views here.
def login(request):
    if request.session.get('is_login',None):
        return redirect('index')


    if request.method == 'POST' :
        login_form = LoginForm(request.POST)
        if login_form.is_valid:
            messages = "请检查填写的内容"
            password = login_form.cleaned_data["login_password"]
            username = login_form.cleaned_data["login_username"]
            print(username,password)



            user = User.objects.get(username=login_form.cleaned_data["login_username"])
            # user.password => 密文
            # password => 明文
            try:
                user = User.objects.get(username = username)

                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                messages = '密码不正确'
                return redirect('register')
            except Exception as e:
                messages = '用户不存在'
            return render(request, 'login.html', locals())
    login_form = LoginForm()
    return render(request,'login.html',locals())


def register(request):
    if request.method == 'POST' :
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid:
            # 绑定数据的表单

            username = reg_form.cleaned_data["reg_username"]
            password = reg_form.cleaned_data["reg_password"]
            email = reg_form.cleaned_dataT["reg_email"]
            same_name = User.objects.filter(username=username)
            if same_name:
                messages = '用户已经存在,请重新选择用户名'
                return render(request,'login.html',locals())
            same_email = User.objects.filter(email=email)
            if same_email:
                messages = '邮箱已被注册,请使用别的邮箱'
                return render(request,'login.html',locals())

            user=User.objects.create(username=username, email=email,password=password)
            user.save()
            return redirect('index')
    reg_form = RegisterForm()
    return render(request, 'login.html', locals())


def logout(request):
    if not request.session.get("is_login"):
        return redirect('login')
    request.session.flush()
    return redirect('login')

