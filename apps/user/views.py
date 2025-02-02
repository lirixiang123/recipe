from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# from .forms import  RegisterForm, LoginForm
from django.urls import reverse
from django.views import View


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



class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.method == 'POST' :
            form = UserCreationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = User.objects.create_user(username= username,password = password)
                user.save()
                if user:
                    request.session['session_id'] = user.pk
                    user = authenticate(username = username,password = password)
                    login(request,user)
                    return redirect('index')
            form = UserCreationForm()
            if form.error_messages:
                errors=form.error_messages
            return render(request,'register.html',locals())

def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

def submit(request):
    return render(request,"submit-recipe.html")

def test(request):
    return render(request,"test.html")

