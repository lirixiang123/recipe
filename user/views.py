from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from .forms import  RegisterForm, LoginForm
from django.urls import reverse
from django.views import View

from .models import User

# Create your views here.
def user_login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password =  request.POST['password1']
        user = authenticate(request,username = username,password = password)
        referer = request.META.get('HTTPS_REFERER','index')
        if user is None:
            messages = "用户不存在"
            return render(request,'login.html',locals())
        else:
            login(request,user)
            return redirect(referer)
    else:
        return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.method == 'POST' :
            form = UserCreationForm(request.POST)
            print(form.error_messages)
            # print(form)
            if form.is_valid():
                form.save()
                username = request.cleaned_data['username']
                password = request.cleaned_data['password1']
                user = authenticate(username = username,password = password)
                if user:
                    request.session['session_id'] = user.pk
                    login(request,user)
                    return redirect('index')
            form = UserCreationForm()
            return render(request,'register.html',locals())

def submit(request):
    return render(request,"submit-recipe.html")

