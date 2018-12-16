from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from bm_project.forms_signup import SignupForm
from bm_project.forms_login import LoginForm
from bm_project.forms_search import SearchForm
from django.contrib.auth import authenticate,login as auth_login
from django.core.paginator import Paginator

# Create your views here.

import hashlib
from .models import Material


def home(request):
    return render(request,'index.html')

def chart(request):
    return render(request,'chart.html')

def searchbyid(request):
    contact_list = Material.matobj.all()
    print(contact_list)
    paginator = Paginator(contact_list, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, "search.html", {'contacts': contacts})


def signup(request):
	path=request.get_full_path()
	if request.method=='POST':
		form=SignupForm(data=request.POST,auto_id="%s")
		if form.is_valid():
			UserModel=get_user_model()
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user=UserModel.objects.create_user(username=username,email=email,password=password)
			user.save()
			auth_user = authenticate(username=username,password=password)
			auth_login(request,auth_user)
			return redirect("home")
	else:
		form=SignupForm(auto_id="%s")
	return render(request, 'signup.html', locals())


def login(request):
    if request.method == 'POST':
        form1 = LoginForm(request.POST)
        if form1.is_valid(): #获取表单信息
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                auth_login(request,user)
                return redirect("home")
            else:
                form1 = LoginForm()
                context = {}
                context['form1'] = form1
                context['errors']="用户名或密码不正确"
                return render(request, 'login1.html', context)
    else:
        form1 =LoginForm()
        context={}
        context['form1']=form1
        return render(request, 'login1.html', context)


def search(request):
    contact_list=Material.matobj.all()
    print(contact_list)
    paginator = Paginator(contact_list, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request,"helllo.html",{'contacts':contacts})

def searchid(request):
    if request.method == 'POST':
        form2=SearchForm(request.POST)
        if form2.is_valid():
            materialid=form2.cleaned_data['materialid']
            print(materialid)
            contact_list = Material.matobj.filter(materialid=materialid)
            paginator = Paginator(contact_list, 2)
            page = request.GET.get('page')
            contacts = paginator.get_page(page)
            context={}
            context['form2']=form2
            context['contacts']=contacts
            return render(request,"search.html",context)
        else:
            form2 = SearchForm()
            context = {}
            context['form2'] = form2
            return render(request, "search.html", context)
    else:
        form2 = SearchForm()
        context = {}
        context['form2'] = form2
        return render(request, "search.html", context)

def home1(request):
    return render(request,'index.html')


