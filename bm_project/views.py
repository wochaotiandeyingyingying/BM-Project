from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from bm_project.forms_signup import SignupForm
from bm_project.forms_login import LoginForm
from bm_project.forms_search import SearchForm
from django.contrib.auth import authenticate,login as auth_login
from django.core.paginator import Paginator
from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.io.vasp.inputs import Incar
from pymatgen.io.vasp.inputs import Poscar
from pymatgen.io.vasp.inputs import Potcar
from pymatgen.io.vasp.inputs import VaspInput
from pymongo import  MongoClient
from pymatgen.core.structure import Structure
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.
import json
from bson import json_util
import hashlib
from .models import Material
import paramiko
import pymongo
import re
from pymongo import MongoClient
import os
#机器学习模块
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.datasets.samples_generator import make_circles
from sklearn.svm import SVC
from django.core import serializers
from sklearn import tree
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import graphviz
# def home(request):
#     return render(request,'index.html')
def rehome(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    return redirect("home")

def searchall_elements(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'search.html',{'username': username,'email':email})
    else:
        return redirect("/door/")

def searchall_formula(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'search2.html',{'username': username,'email':email})
    else:
        return redirect("/door/")


def searchall_ids(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'search3.html',{'username': username,'email':email})
    else:
        return redirect("/door/")


def chart(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'chart.html',{'username': username,'email':email})
    else:
        return redirect("/door/")

def introduction(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'introduction.html',{'username': username,'email':email})
    else:
        return redirect("/door/")




@csrf_exempt
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
            request.session['IS_LOGIN'] = True
            request.session['USRNAME'] = username
            request.session['EMAIL'] = email
            address='./User/'+username
            os.mkdir(address)
            print('创建成功')
            return redirect("home")
    else:
        form = SignupForm(auto_id="%s")
    return render(request, 'signup.html', locals())

@csrf_exempt
def login(request):
    if request.method == 'POST':
        form1 = LoginForm(request.POST)
        if form1.is_valid(): #获取表单信息
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                auth_login(request,user)
                request.session['IS_LOGIN'] = True
                request.session['USRNAME'] = username
                request.session['EMAIL'] = request.user.email
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
def door(request):
    return render(request,'door.html')
def home(request):
     username = request.session.get('USRNAME', False)
     is_login = request.session.get('IS_LOGIN',False)
     email = request.session.get('EMAIL', False)
     print(is_login)
     if is_login:
         return render(request, 'index.html',{'username': username,'email':email})
     else:
         return redirect("/door/")


# def searchid(request):
#     if request.method == 'POST':
#         form2=SearchForm(request.POST)
#         if form2.is_valid():
#             materialid=form2.cleaned_data['materialid']
#             print(materialid)
#             contact_list = Material.matobj.filter(materialid=materialid)
#             # contact_list=Material.matobj.filter(type_name_icontains='')模糊查询
#             paginator = Paginator(contact_list, 2)
#             page = request.GET.get('page')
#             contacts = paginator.get_page(page)
#             context={}
#             context['form2']=form2
#             context['contacts']=contacts
#             return render(request,"search.html",context)
#         else:
#             form2 = SearchForm()
#             context = {}
#             context['form2'] = form2
#             return render(request, "search.html", context)
#     else:
#         form2 = SearchForm()
#         context = {}
#         context['form2'] = form2
#         return render(request, "search.html", context)

def search_id(request):
    is_login = request.session.get('IS_LOGIN', False)
    email = request.session.get('EMAIL', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        materialid = request.POST.get('materialid')
        contact_list = Material.matobj.filter(slid=materialid)
        paginator = Paginator(contact_list, 10)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, "search3.html", {'contacts': contacts,'username': username,'email':email})
    else:
        return redirect("/door/")


def search_elements(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        a = ''
        if request.method == 'POST':
            a = request.POST['elements']
        else:
            a = request.GET.get('elements')

        a0 = ''
        a1 = ''
        a2 = ''
        a3 = ''
        a4 = ''
        a5 = ''
        a6 = ''
        a7 = ''
        b = [a0, a1, a2, a3, a4, a5, a6, a7]
        m = -1
        for i in a:
            if 'A' <= i <= 'Z':
                m = m + 1
                b[m] = b[m] + i
            elif i!='-':
                b[m] = b[m] + i
        for i in range(0,8):
            print(b[i])
        client = MongoClient('39.108.210.141', 27017)

        db_name = 'BM_Project'
        db = client[db_name]
        contact_list = db.material.find(
            {"$and": [{"elements": {'$regex': b[0]}}, {"elements": {'$regex': b[1]}}, {"elements": {'$regex': b[2]}},
                      {"elements": {'$regex': b[3]}}, {"elements": {'$regex': b[4]}}, {"elements": {'$regex': b[5]}},
                      {"elements": {'$regex': b[6]}}, {"elements": {'$regex': b[7]}}]})

        array = list(contact_list)
        paginator = Paginator(array, 10)
        print(paginator)
        page = request.GET.get('page')
        print(page)
        contacts = paginator.get_page(page)
        print(contacts)
        print(a)
        return render(request, "search.html", {'contacts': contacts , 'elements': a,'username': username,'email':email})
    else:
        return redirect("/door/")


def search_formula(request):
    is_login = request.session.get('IS_LOGIN', False)
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    print(is_login)
    if is_login:
        prettyformula = request.POST.get('prettyformula')
        print(prettyformula)
        contact_list = Material.matobj.filter(prettyformula=prettyformula)
        print(contact_list)
        paginator = Paginator(contact_list, 10)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, "search2.html", {'contacts': contacts,'username': username,'email':email})
    else:
        return redirect("/door/")
@csrf_exempt
def vasp(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    slid=request.POST.get('slid')
    servername=request.session.get('SERVERNAME',False)
    serverpassword=request.session.get('SERVERPASSWORD',False)
    if(servername==False or serverpassword==False):
        return redirect("/serverinput/")

    contact_list = Material.matobj.filter(slid=slid)
    print(contact_list)
    paginator = Paginator(contact_list, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, "search3.html", {'contacts': contacts, 'username': username, 'email':email})
@csrf_exempt
def serverinput(request):
    if request.method == 'POST':
        form1 = LoginForm(request.POST)
        if form1.is_valid():  # 获取表单信息
            servername = form1.cleaned_data['username']
            serverpassword = form1.cleaned_data['password']
            try:
                ssh = paramiko.SSHClient()
                policy = paramiko.AutoAddPolicy()
                ssh.set_missing_host_key_policy(policy)
                ssh.connect(
                    hostname="172.26.18.243",  # 服务器的ip
                    port=22,  # 服务器的端口
                    username=servername,  # 服务器的用户名
                    password=serverpassword,  # 用户名对应的密码
                )
                request.session['SERVERNAME'] = servername
                request.session['SERVERPASSWORD'] = serverpassword
                return redirect("../")
            except BaseException as e:
                form1 = LoginForm()
                context = {}
                context['form1'] = form1
                context['errors'] = "用户名或密码不正确"
                return render(request, 'serverinput.html', context)
    else:
        form1 = LoginForm()
        context = {}
        context['form1'] = form1
        return render(request, 'serverinput.html', context)


@csrf_exempt
def high_throughput(request):
    is_login = request.session.get('IS_LOGIN', False)
    email = request.session.get('EMAIL', False)
    servername = request.session.get('SERVERNAME', False)
    serverpassword = request.session.get('SERVERPASSWORD', False)
    if (servername == False or serverpassword == False):
        return redirect("/serverinput/")
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        if request.is_ajax():
            a = request.POST.get('slid')
            print(a)
            a0 = ''
            a1 = ''
            a2 = ''
            a3 = ''
            a4 = ''
            a5 = ''
            a6 = ''
            a7 = ''
            b = [a0, a1, a2, a3, a4, a5, a6, a7]
            m = -1
            for i in a:
                if 'A' <= i <= 'Z':
                    m = m + 1
                    b[m] = b[m] + i
                elif i != '-':
                    b[m] = b[m] + i
            for i in range(0, 8):
                print(b[i])
            client = MongoClient('39.108.210.141', 27017)

            db_name = 'BM_Project'
            db = client[db_name]
            contact_list = db.material.find(
                {"$and": [{"elements": {'$regex': b[0]}}, {"elements": {'$regex': b[1]}},
                          {"elements": {'$regex': b[2]}},
                          {"elements": {'$regex': b[3]}}, {"elements": {'$regex': b[4]}},
                          {"elements": {'$regex': b[5]}},
                          {"elements": {'$regex': b[6]}}, {"elements": {'$regex': b[7]}}]})

            array = list(contact_list)
            #data = json.dumps(array, ensure_ascii=False)
            data=json_util.dumps(array)

            #data['list'] = json.loads(serializers.serialize("json", array))
            print(data)
            return JsonResponse(data,safe=False)
        else:
            return render(request, "high_throughput.html", {'username': username, 'email': email})
    else:
        return redirect("/door/")
def readytovasp(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    slid = request.GET.get('slid')
    return render(request, "readytovaspnew.html",{'slid':slid,'username': username,'email':email})
@csrf_exempt
def automatic(request):
    try:
    #获得了前台传过来的id
        print('进来了啊？')
        client = MongoClient('39.108.210.141', 27017)  #
        mydb = client.BM_Project  # 连接所需数据库,db为数建立MongoDB数据库连接据库名
        collection = mydb.material  # 连接所用集合，也就是我们通常所说的表，local为表名
        def getstructure(a):
            b = collection.find_one({"slid": a}, {'structure': 1})
            b = b['structure']
            structure = Structure.from_dict(b)
            return structure
        def getkpoints(structure):
            k = Kpoints.automatic_density(structure, 1000)
            print('kpoints')
            return k
        def getposcar(structure):
            ps = Poscar(structure)
            print('getposcar')
            return ps
        def getpotcar(poscar,potcarop):
            Poscar.write_file(poscar, 'testposcar')  # 把poscar写成了一个文件
            with open("testposcar") as file_object:
                lines = file_object.readlines()  # 创建一个包含文件各行内容的列表
                potcarline = lines[5]  # 得到了poscar的有关potcar的序列
            num = potcarline.count(' ') + 1  # 获得空格数量，方便之后的分解
            a0 = ''
            a1 = ''
            a2 = ''
            a3 = ''
            a4 = ''
            a5 = ''
            b = [a0, a1, a2, a3, a4, a5]
            for i in range(0, num):
                b[i] = potcarline.split(' ', 1)[0]
                b[i] = b[i].replace("\n", "")  # 去掉末尾的换行符
                num = num - 1
                if num != 0:
                    potcarline = potcarline.split(' ', 1)[1]
            ofile = open('temp-test', 'w')
            for i in range(0, 6):
                if len(b[i]) != 0:
                    print(b[i])
                    if potcarop=='pwe':
                        for txt in open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\potcar-first\\POTCAR-' + b[i], 'r'):
                            ofile.write(txt)
                    elif potcarop=='gga':
                        for txt in open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\potcar-gga\\POTCAR-' + b[i], 'r'):
                            ofile.write(txt)
                    elif potcarop=='lda':
                        for txt in open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\potcar-lda\\POTCAR-' + b[i], 'r'):
                            ofile.write(txt)
            ofile.close()  # 得到了合成之后的potcar文件
            pt = Potcar.from_file('temp-test')
            print('getpotcar')
            return pt
        def gotovasp(i, k, ps, pt,materialid,jobscript):
            z = VaspInput(i, k, ps, pt)
            os.remove('temp-test')  # 删除刚才生成的poscar的临时文件
            os.remove('testposcar')
            username = request.session.get('USRNAME', False)
            #获得编号
            with open('./count.txt', 'r+') as f:
                counttext = f.read()
                count = int(counttext) + 1
                f.seek(0)
                f.truncate()  # 清空文件
                f.write(str(count))  # 重新写入新的访问量
                f.flush()
                f.close()
            print(count)
            #编号结束
            #获得文件名
            print(materialid)

            filename = 'task-' + str(count) + materialid
            print(filename)
            #文件名结束
            #获得路径
            address = './User/' + username + '/'+filename
            #获得路径结束
            print(address)
            VaspInput.write_input(z, output_dir=address)
            jobaddress = address + '/job'
            print(jobaddress)
            with open(jobaddress, 'w') as destination:
                destination.write(jobscript)
                destination.close()
            return count


        if request.is_ajax :
            print('看看好了没')
            try:
                potcarop = request.POST.get("Potcar")
            except BaseException as e:
                with open('testlog1', 'wb') as destination:
                    e = str(e)
                    e = e.encode()
                    destination.write(e)
                destination.close()
            incar = request.POST.get("Level")
            jobscript=request.POST.get("Levell")
            materialid = request.POST.get('materialid')
            incar1=request.POST.get('Incar1')
            incar2 = request.POST.get('Incar2')
            incar3 = request.POST.get('Incar3')
            incar4 = request.POST.get('Incar4')
            incar5 = request.POST.get('Incar5')
            jobscript1=request.POST.get('jobscript1')
            jobscript2 = request.POST.get('jobscript2')
            jobscript3 = request.POST.get('jobscript3')
            jobscript4 = request.POST.get('jobscript4')
            print('进来了吗')
            print(jobscript1)
            print(jobscript)
            if jobscript=='25':
                jobscript=jobscript1
            elif jobscript=='50':
                jobscript=jobscript2
            elif jobscript=='75':
                jobscript=jobscript3
            elif jobscript=='100':
                jobscript=jobscript4
            if incar == '1':
                incar=incar1
            elif incar == '2':
                incar = incar2
            elif incar == '3':
                incar = incar3
            elif incar == '4':
                incar = incar4
            elif incar == '5':
                incar = incar5
            print('是否到前面了')
            print('开始potcar')
            print(potcarop)
            print('开始incar')
            print(incar)
            print('开始jobscript')
            print(jobscript)
            print('开始materialid')
            print(materialid)

            if potcarop!=None and incar!=None and jobscript!=None and materialid!=None:
                structure = getstructure(materialid)
                poscar = getposcar(structure)
                kpoints = getkpoints(structure)
                potcar = getpotcar(poscar,potcarop)
                i=Incar.from_string(incar)
                count=gotovasp(i, kpoints, poscar, potcar,materialid,jobscript)
                username = request.session.get('USRNAME', False)
                servername = request.session.get('SERVERNAME', False)
                serverpassword = request.session.get('SERVERPASSWORD', False)
                ssh = paramiko.SSHClient()
                # # 创建默认的白名单
                policy = paramiko.AutoAddPolicy()
                # # 设置白名单
                ssh.set_missing_host_key_policy(policy)
                # # 链接服务器
                ssh.connect(
                    hostname="172.26.18.243",  # 服务器的ip
                    port=22,  # 服务器的端口
                    username=servername,  # 服务器的用户名
                    password=serverpassword  # 用户名对应的密码
                )
                filename = 'task-' + str(count) + materialid
                address = '/gpfs/home/gromacs/BM/User/' + username + '/' + filename
                cmd1 = 'cp /gpfs/home/gromacs/common/test2.py  ' + address
                cmd2 = 'cd ' + address + ';python test2.py'
                cmd3='cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/task-28sl-0;python test2.py'
                cmd4='cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/task-28sl-0;export PATH=$PATH:/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_SERVERDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/etc;LSF_LIBDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/lib;export LSF_VERSION=10.0;export LSF_BINDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_ENVDIR=/gpfs/lsf/conf;bsub<job'
                #ssh.exec_command(cmd1)
                ssh.exec_command(cmd4)

                #服务器操作
                # ssh = paramiko.SSHClient()
                # # 创建默认的白名单
                # policy = paramiko.AutoAddPolicy()
                # # 设置白名单
                # ssh.set_missing_host_key_policy(policy)
                # # 链接服务器
                # ssh.connect(
                #     hostname="172.26.18.243",  # 服务器的ip
                #     port=22,  # 服务器的端口
                #     username="gromacs",  # 服务器的用户名
                #     password="gromacs"  # 用户名对应的密码
                # )
                # cmd = 'cd /gpfs/home/gromacs/123/ABCd ;dos2unix /gpfs/home/gromacs/123/ABCd/job ; bsub<job'
                # ssh.exec_command(cmd)
                print('真的成功了吗')
                #return render(request, 'go_home.html')
                data='1'
                return JsonResponse(data, safe=False)
            else:
                print('失败')
    except BaseException as e:
        with open('testlog', 'wb') as destination:
            e = str(e)
            e = e.encode()
            destination.write(e)
        destination.close()






        #n=Poscar.from_file(t4)
        #print(n)
        #可以返回选项值了
@csrf_exempt
def manual(request):
    try:
        def gotovasp(i, k, ps, pt,materialid,t5):
            z = VaspInput(i, k, ps, pt)
            os.remove('./testpotcar')  # 删除刚才生成的poscar的临时文件
            os.remove('./testposcar')
            os.remove('./testkpoints')
            os.remove('./testincar')
            with open('./count.txt', 'r+') as f:
                counttext = f.read()
                count = int(counttext) + 1
                f.seek(0)
                f.truncate()  # 清空文件
                f.write(str(count))  # 重新写入新的访问量
                f.flush()
                f.close()
            print(count)
            #编号结束
            #获得文件名
            print(materialid)

            filename = 'task-' + str(count) + materialid
            print(filename)
            #文件名结束
            #获得路径
            username = request.session.get('USRNAME', False)

            address = './User/' + username + '/'+filename
            #获得路径结束
            print(address)
            VaspInput.write_input(z, output_dir=address)
            jobaddress = address + '/job'
            print(jobaddress)
            with open(jobaddress, 'w') as destination:
                for chunk in t5.chunks():
                    chunk = chunk.decode("utf-8")
                    destination.write(chunk)
            destination.close()
        if request.method == "POST":
            t1 =request.FILES.get('potcar')
            t2 = request.FILES.get("poscar", None)
            t3 = request.FILES.get("kpoints", None)
            t4 = request.FILES.get("incar", None)
            t5 = request.FILES.get("jobscript", None)
        if t1!=None and t2!=None and t3!=None and t4!=None:
            with open('./testpotcar', 'wb+') as destination:
                for chunk in t1.chunks():
                    destination.write(chunk)
            potcar=Potcar.from_file('./testpotcar')
            with open('./testposcar', 'wb+') as destination:
                for chunk in t2.chunks():
                    destination.write(chunk)
            poscar = Poscar.from_file('./testposcar')
            with open('./testkpoints', 'wb+') as destination:
                for chunk in t3.chunks():
                    destination.write(chunk)
            kpoints = Kpoints.from_file('./testkpoints')
            with open('./testincar', 'wb+') as destination:
                for chunk in t4.chunks():
                    destination.write(chunk)
            incar = Incar.from_file('./testincar')
            materialid = request.POST['materialid']
            gotovasp(incar, kpoints, poscar, potcar,materialid,t5)
            # ssh = paramiko.SSHClient()
            # # 创建默认的白名单
            # policy = paramiko.AutoAddPolicy()
            # # 设置白名单
            # ssh.set_missing_host_key_policy(policy)
            # # 链接服务器
            # ssh.connect(
            #     hostname="172.26.18.243",  # 服务器的ip
            #     port=22,  # 服务器的端口
            #     username="gromacs",  # 服务器的用户名
            #     password="gromacs"  # 用户名对应的密码
            # )
            # cmd = 'cd /gpfs/home/gromacs/123/ABCd ; dos2unix /gpfs/home/gromacs/123/ABCd/job ;bsub<job'
            # ssh.exec_command(cmd)
            #return redirect("home")
    except BaseException as e:
        with open('testlog', 'wb') as destination:
            e = str(e)
            e = e.encode()
            destination.write(e)
        destination.close()

def taskmanage(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)

        return render(request, 'taskmanage.html',{'username':username,'email':email})
    else:
        return redirect("/door/")
def logout(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:

        del request.session['USRNAME']

        del request.session['EMAIL']
        del request.session['IS_LOGIN']
        del request.session['SERVERNAME']
        del request.session['SERVERPASSWORD']
        return redirect("/login/")
    else:
        return redirect("/door/")
def getCount():#获取访问次数
    with open('count.txt', 'r+') as f:
        counttext = f.read()
        count = int(counttext) + 1
        f.seek(0)
        f.truncate()  # 清空文件
        f.write(str(count))  # 重新写入新的访问量
        f.flush()
        f.close()
    return count
def getFilename(materialid):
    count=getCount()
    filename='task-'+count+materialid
    return filename
def materialdetail(request):
    slid = request.GET.get('slid')
    print(slid)
    contact_list = Material.matobj.filter(slid=slid)
    paginator = Paginator(contact_list, 10)
    contacts = paginator.get_page('1')
    print('begin')
    print(contacts)
    return render(request, "structure.html", {'contacts': contacts})
def her_data(request):
    is_login = request.session.get('IS_LOGIN', False)
    slid = request.GET.get('slid')
    if request.method=="POST":
        insertid = request.POST["id"]
        insertslid=request.POST["insertslid"]
        prettyformula = request.POST["prettyformula"]
        elements = request.POST["elements"]
        if (insertid != None and insertslid != None and prettyformula != None and elements != None):
            creat = Material.matobj.create(id=insertid, slid=insertslid, prettyformula=prettyformula, elements=elements)
            creat.save()
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        if(slid!=None):
            delete=Material.matobj.filter(slid=slid)
            delete.delete()
        contact_list = Material.matobj.filter()
        id=Material.matobj.last().id+1
        paginator = Paginator(contact_list, 10)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        if username=='aning':
            hidden=''
        else:
            hidden='none'
        return render(request, 'her_data.html', {'contacts': contacts,'username': username, 'email': email,'hidden':hidden,'id':id})
    else:
        return redirect("/door/")
def svc(request):
    if request.method == 'POST':
        c = float(request.POST.get('C'))
        degree = float(request.POST.get('degree'))
        gamma = float(request.POST.get('gamma'))
        coef0 = float(request.POST.get('coef0'))
        max_itera = float(request.POST.get('max_iter'))
        print(c)
        print(type(c))
        #机器学习代码开始
        x, y = make_circles(200, factor=.1, noise=.2)
        # model = SVC(kernel='linear')#线性可分
        model = SVC(kernel='rbf', C=c, gamma=gamma, degree=degree, coef0=coef0, max_iter=max_itera)
        model.fit(x, y)
        def plot_svc(model, ax=None, plot_support=True):
            if ax is None:
                ax = plt.gca()
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            x = np.linspace(xlim[0], xlim[1], 30)
            y = np.linspace(ylim[0], ylim[1], 30)
            Y, X = np.meshgrid(y, x)
            xy = np.vstack([X.ravel(), Y.ravel()]).T
            p = model.decision_function(xy).reshape(X.shape)
            ax.contour(X, Y, p, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
            if plot_support:
                ax.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=300, linewidths=1,
                           facecolors='none')

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

        plt.scatter(x[:, 0], x[:, 1], c=y, s=50, cmap='autumn')
        plot_svc(model)
        plt.savefig('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\static\\css\\picture\\comment.png')
        return render(request, "result.html")
    else:
        return render(request, "svc.html")
def dtc(request):
    if request.method == 'POST':
        min_impurity_decrease = int(request.POST.get('min_impurity_decrease'))
        min_samples_leaf = int(request.POST.get('min_samples_leaf'))
        min_samples_split = int(request.POST.get('min_samples_split'))
        max_depth = int(request.POST.get('max_depth'))
        random_state = int(request.POST.get('random_state'))
        #机器学习代码开始
        wine = load_wine()
        wine1 = pd.concat([pd.DataFrame(wine.data), pd.DataFrame(wine.target)], axis=1)
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(wine.data, wine.target, test_size=0.3)  # 分训练集和测试集
        clf = tree.DecisionTreeClassifier(criterion="entropy",
                                          random_state=random_state,
                                          splitter="random",
                                          max_depth=max_depth,  # 建议从3开始
                                          min_samples_split=min_samples_split,
                                          min_samples_leaf=min_samples_leaf,#防止过拟合
                                          min_impurity_decrease=min_impurity_decrease,  # 信息增益
                                          )  # 实例化，目前这些端口就应该够了
        clf = clf.fit(Xtrain, Ytrain)  # 用训练集数据训练模型
        result = clf.score(Xtest, Ytest)
        test = []
        for i in range(10):
            clf = tree.DecisionTreeClassifier(max_depth=i + 1, criterion="entropy", random_state=30, splitter="random")
            clf = clf.fit(Xtrain, Ytrain)
            score = clf.score(Xtest, Ytest)
            test.append(score)
        plt.plot(range(1, 11), test, color="red", label="max_depth")
        plt.legend()
        plt.savefig('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\static\\css\\picture\\comment1.png')
        return render(request, "result1.html")
    else:
        return render(request, "dtc.html")

def readytohigh_throughput(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    if request.method == 'POST':
        c = request.POST.get('vaspid')
        array=[]
        num=0
        for i in c:
            if i==',':
                num=num+1
    return render(request, "readytohigh_throughput.html",{'num':num,'username': username,'email':email,'c':c})
def high_throughput_go(request):
    if request.method == 'POST':
        slid = request.GET.get('c')
        array=[]
        num=0
        for i in slid:
            if i==',':
                num=num+1
        for i in range(0,num):
            temp=slid.split(',',1)[0]
            array.append(temp)
            slid=slid.split(',',1)[1]
    try:
        client = MongoClient('39.108.210.141', 27017)  #
        mydb = client.BM_Project  # 连接所需数据库,db为数建立MongoDB数据库连接据库名
        collection = mydb.material  # 连接所用集合，也就是我们通常所说的表，local为表名
        def getstructure(a):
            b = collection.find_one({"slid": a}, {'structure': 1})
            b = b['structure']
            structure = Structure.from_dict(b)
            return structure
        def getkpoints(structure):
            k = Kpoints.automatic_density(structure, 1000)
            print('kpoints')
            return k
        def getposcar(structure):
            ps = Poscar(structure)
            print('getposcar')
            return ps
        def getpotcar(poscar,potcarop):
            Poscar.write_file(poscar, 'testposcar')  # 把poscar写成了一个文件
            with open("testposcar") as file_object:
                lines = file_object.readlines()  # 创建一个包含文件各行内容的列表
                potcarline = lines[5]  # 得到了poscar的有关potcar的序列
            num = potcarline.count(' ') + 1  # 获得空格数量，方便之后的分解
            a0 = ''
            a1 = ''
            a2 = ''
            a3 = ''
            a4 = ''
            a5 = ''
            b = [a0, a1, a2, a3, a4, a5]
            for i in range(0, num):
                b[i] = potcarline.split(' ', 1)[0]
                b[i] = b[i].replace("\n", "")  # 去掉末尾的换行符
                num = num - 1
                if num != 0:
                    potcarline = potcarline.split(' ', 1)[1]
            ofile = open('temp-test', 'w')
            for i in range(0, 6):
                if len(b[i]) != 0:
                    print(b[i])
                    if potcarop=='pwe':
                        for txt in open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\potcar-first\\POTCAR-' + b[i], 'r'):
                            ofile.write(txt)
                    elif potcarop=='gga':
                        for txt in open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\potcar-gga\\POTCAR-' + b[i], 'r'):
                            ofile.write(txt)
                    elif potcarop=='lda':
                        for txt in open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\potcar-lda\\POTCAR-' + b[i], 'r'):
                            ofile.write(txt)
            ofile.close()  # 得到了合成之后的potcar文件
            pt = Potcar.from_file('temp-test')
            print('getpotcar')
            return pt
        def gotovasp(i, k, ps, pt,materialid,jobscript):
            print('aaaaa')
            z = VaspInput(i, k, ps, pt)
            print('bbbbbb')
            os.remove('temp-test')  # 删除刚才生成的poscar的临时文件
            os.remove('testposcar')
            username = request.session.get('USRNAME', False)
            print('ccccc')
            #获得编号
            with open('./count.txt', 'r+') as f:
                counttext = f.read()
                count = int(counttext) + 1
                f.seek(0)
                f.truncate()  # 清空文件
                f.write(str(count))  # 重新写入新的访问量
                f.flush()
                f.close()
            print('ddddd')
            print(count)
            #编号结束
            #获得文件名
            print(materialid)

            filename = 'task-' + str(count) + materialid
            print(filename)
            #文件名结束
            #获得路径
            address = './User/' + username + '/'+filename
            #获得路径结束
            print(address)
            VaspInput.write_input(z, output_dir=address)
            jobaddress = address + '/job'
            with open(jobaddress, 'w') as destination:
                destination.write(jobscript)
                destination.close()
            return count


        if request.method == "POST":
            potcarop = request.POST["Potcar"]
            incar = request.POST["Level"]
            jobscript=request.POST["Levell"]
            materialid = request.POST['materialid']
            incar1=request.POST['Incar1']
            incar2 = request.POST['Incar2']
            incar3 = request.POST['Incar3']
            incar4 = request.POST['Incar4']
            incar5 = request.POST['Incar5']
            jobscript1=request.POST['jobscript1']
            jobscript2 = request.POST['jobscript2']
            jobscript3 = request.POST['jobscript3']
            jobscript4 = request.POST['jobscript4']
            if jobscript=='25':
                jobscript=jobscript1
            elif jobscript=='50':
                jobscript=jobscript2
            elif jobscript=='75':
                jobscript=jobscript3
            elif jobscript=='100':
                jobscript=jobscript4
            if incar == '1':
                incar=incar1
            elif incar == '2':
                incar = incar2
            elif incar == '3':
                incar = incar3
            elif incar == '4':
                incar = incar4
            elif incar == '5':
                incar = incar5
            for i in range(0,num):
                print('开始')
                print(num)
                materialid=array[i]
                if potcarop!=None and incar!=None and jobscript!=None and array[i]!=None:
                    print('结束')
                    structure = getstructure(array[i])
                    poscar = getposcar(structure)
                    kpoints = getkpoints(structure)
                    potcar = getpotcar(poscar,potcarop)
                    i=Incar.from_string(incar)
                    count=gotovasp(i, kpoints, poscar, potcar,materialid,jobscript)

                    username = request.session.get('USRNAME', False)
                    servername = request.session.get('SERVERNAME', False)
                    serverpassword = request.session.get('SERVERPASSWORD', False)

                    ssh = paramiko.SSHClient()
                    # # 创建默认的白名单
                    policy = paramiko.AutoAddPolicy()
                    # # 设置白名单
                    ssh.set_missing_host_key_policy(policy)
                    # # 链接服务器
                    ssh.connect(
                        hostname="172.26.18.243",  # 服务器的ip
                        port=22,  # 服务器的端口
                        username=servername,  # 服务器的用户名
                        password=serverpassword  # 用户名对应的密码
                    )
                    filename = 'task-' + str(count) + materialid
                    address = '/gpfs/home/gromacs/BM/User/' + username + '/' + filename
                    cmd1 = 'cp /gpfs/home/gromacs/common/test2.py  ' + address
                    cmd2 = 'cd ' + address + ';python test2.py'
                    cmd3='cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/task-28sl-0;python test2.py'
                    cmd4='cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/task-28sl-0;export PATH=$PATH:/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_SERVERDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/etc;LSF_LIBDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/lib;export LSF_VERSION=10.0;export LSF_BINDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_ENVDIR=/gpfs/lsf/conf;bsub<job'
                    cmd5='cd '+address+';export PATH=$PATH:/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_SERVERDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/etc;LSF_LIBDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/lib;export LSF_VERSION=10.0;export LSF_BINDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_ENVDIR=/gpfs/lsf/conf;bsub<job'

                    ssh.exec_command(cmd5)

                    #服务器操作
                    # ssh = paramiko.SSHClient()
                    # # 创建默认的白名单
                    # policy = paramiko.AutoAddPolicy()
                    # # 设置白名单
                    # ssh.set_missing_host_key_policy(policy)
                    # # 链接服务器
                    # ssh.connect(
                    #     hostname="172.26.18.243",  # 服务器的ip
                    #     port=22,  # 服务器的端口
                    #     username="gromacs",  # 服务器的用户名
                    #     password="gromacs"  # 用户名对应的密码
                    # )
                    # cmd = 'cd /gpfs/home/gromacs/123/ABCd ;dos2unix /gpfs/home/gromacs/123/ABCd/job ; bsub<job'
                    # ssh.exec_command(cmd)

                else:
                    print('失败')
            return redirect("home")
    except BaseException as e:
        with open('testlog', 'wb') as destination:
            e = str(e)
            e = e.encode()
            destination.write(e)
    destination.close()
def tutorials(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'maps.html',{'username': username,'email':email})
    else:
        return redirect("/door/")












