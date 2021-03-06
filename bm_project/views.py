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
from pymatgen.core.structure import Structure
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import re
# Create your views here.
import json
from bson import json_util
import hashlib
from .models import Material
import paramiko
import pymongo
import re
from pymongo import MongoClient

import socket
import os
from django.http import FileResponse
import time
import os
#机器学习模块
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.datasets.samples_generator import make_circles
from sklearn.svm import SVC
from django.core import serializers
from sklearn import tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import csv
import joblib
import datetime
from pandas import DataFrame
from playml.linearR import linearR
from sklearn.linear_model import LinearRegression
#用于返回主界面的方式
def rehome(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    return redirect("home")
#返回搜索元素的界面
def searchall_elements(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'search.html',{'username': username,'email':email})
    else:
        return redirect("/door/")
#返回搜索化学式的界面
def searchall_formula(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'search2.html',{'username': username,'email':email})
    else:
        return redirect("/door/")

#返回搜索材料id的界面
def searchall_ids(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'search3.html',{'username': username,'email':email})
    else:
        return redirect("/door/")

#返回图表界面
def chart(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'chart.html',{'username': username,'email':email})
    else:
        return redirect("/door/")
#返回
def introduction(request):
    is_login = request.session.get('IS_LOGIN', False)
    print(is_login)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'introduction.html',{'username': username,'email':email})
    else:
        return redirect("/door/")



#用户注册界面
@csrf_exempt
def signup(request):
    try:
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
                address1='./User/'+username
                address2 = './User/' + username+'-ml'
                os.mkdir(address1)
                os.mkdir(address2)
                print('创建成功')
                return redirect("home")
        else:
            form = SignupForm(auto_id="%s")
        return render(request, 'signup.html', locals())
    except BaseException as e:
        with open('testlog', 'wb') as destination:
            e = str(e)
            e = e.encode()
            destination.write(e)
        destination.close()

#用户登录界面
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
#门户界面
def door(request):
    return render(request,'door.html')
#主界面
def home(request):
     username = request.session.get('USRNAME', False)
     is_login = request.session.get('IS_LOGIN',False)
     email = request.session.get('EMAIL', False)
     print(is_login)
     if is_login:
         return render(request, 'index.html',{'username': username,'email':email})
     else:
         return redirect("/door/")



#通过材料编号进行搜索
def search_id(request):
    is_login = request.session.get('IS_LOGIN', False)
    email = request.session.get('EMAIL', False)
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
#通过材料元素进行搜索
#由于特殊性，这个代码用pymongo写的，并没有使用django自带的包
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

#通过化学式进行搜索
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
#点击VASP跳转的界面
@csrf_exempt
def vasp(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    slid=request.POST.get('slid')
    #这里需要判定用户有没有输入服务器的用户名和密码
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
#用户输入服务器的用户名和密码的界面
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

#高通量的选择物质界面，因为这块也是元素组成搜索，所以也是用pymongo写的
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
            print(array)

            #data = json.dumps(array, ensure_ascii=False)
            data=json_util.dumps(array)

            #data['list'] = json.loads(serializers.serialize("json", array))
            print(data)
            return JsonResponse(data,safe=False)
        else:
            return render(request, "high_throughput.html", {'username': username, 'email': email})
    else:
        return redirect("/door/")
#用户选择完物质之后进入到4个输入文件编辑的跳转函数
def readytovasp(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    slid = request.GET.get('slid')
    return render(request, "readytovaspnew.html",{'slid':slid,'username': username,'email':email})
@csrf_exempt
#VASP自动方式提交作业的代码
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
            print('检查potcar的内容开始')
            print(num)
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
            print('a的值')
            print(a0,a1,a2,a3,a4,a5)
            print(b[0],b[1],b[2],b[3],b[4],b[5])
            ofile = open('temp-test', 'w')
            for i in range(0, 6):
                if len(b[i]) != 0:
                    print('B[i]的值')
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
            client = MongoClient('39.108.210.141', 27017)
            mydb = client.BM_Project  # 连接所需数据库,db为数建立MongoDB数据库连接据库名
            collection = mydb.material
            contact_list = collection.find_one({"slid":materialid}, {'prettyformula': 1})
            filename = 'task-' + str(count) + '-'+materialid+ '-'+contact_list['prettyformula']
            print('文件名如下')
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
                client = MongoClient('39.108.210.141', 27017)
                mydb = client.BM_Project  # 连接所需数据库,db为数建立MongoDB数据库连接据库名
                collection = mydb.material
                contact_list = collection.find_one({"slid": materialid}, {'prettyformula': 1})
                filename = 'task-' + str(count) + '-' + materialid + '-' + contact_list['prettyformula']
                address = '/gpfs/home/gromacs/BM/User/' + username + '/' + filename
                cmd1 = 'cp /gpfs/home/gromacs/common/test2.py  ' + address
                cmd2 = 'cd ' + address + ';python test2.py'
                cmd3='cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/task-28sl-0;python test2.py'
                cmd4='cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/task-28sl-0;export PATH=$PATH:/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_SERVERDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/etc;LSF_LIBDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/lib;export LSF_VERSION=10.0;export LSF_BINDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_ENVDIR=/gpfs/lsf/conf;bsub<job'
                #ssh.exec_command(cmd1)
                stdin, stdout, stderr = ssh.exec_command(cmd4)
                temp = stdout.read()
                temp=temp.decode()
                first=temp.find('<')+1
                last=temp.find('>')
                num=temp[first:last]
                filenamenew=filename+'-'+num
                cmd5='cd /gpfs/home/gromacs/BM/User/xiaoxiaobo;mv '+filename+' '+filenamenew
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
                print('真的成功了吗')
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
#用户手动提交4个输入文件进行VASP运算的代码，这个和自动的方式有还有地方没有同意，自动是完善的
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
    except BaseException as e:
        with open('testlog', 'wb') as destination:
            e = str(e)
            e = e.encode()
            destination.write(e)
        destination.close()
#任务运行界面，也是默认的界面
@csrf_exempt
def taskmanage(request):
    print('进入到了运行界面')
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        if request.is_ajax():
            #与服务器建立连接
            ssh = paramiko.SSHClient()
            policy = paramiko.AutoAddPolicy()
            ssh.set_missing_host_key_policy(policy)
            ssh.connect(
                hostname="172.26.18.243",  # 服务器的ip
                port=22,  # 服务器的端口
                username="gromacs",  # 服务器的用户名
                password="gromacs"  # 用户名对应的密码
            )
            #linux命令，分别获得bjobs的结果，用户所有的文件名
            b = 'export PATH=$PATH:/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_SERVERDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/etc;LSF_LIBDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/lib;export LSF_VERSION=10.0;export LSF_BINDIR=/gpfs/lsf/10.1/linux3.10-glibc2.17-x86_64/bin;export LSF_ENVDIR=/gpfs/lsf/conf;bjobs'
            c = 'cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/;ls'
            # 查询bjobs的结果
            stdin,stdout,stderr = ssh.exec_command(b)
            temp1=stdout.read()
            temp1 = temp1.decode()
            #now_job_num是正在运行的作业号的list
            now_job_num=re.findall('[0-9][0-9]{5}',temp1)
            print('now_job_num')
            print(temp1)
            print(now_job_num)
            # 查询用户文件夹的结果
            stdin, stdout, stderr = ssh.exec_command(c)
            temp2= stdout.read()
            temp2 = temp2.decode()
            print('aaaaa'+temp2)
            print('文件名如下')
            print(b)
            result = temp2
            num = temp2.count('\n')
            print('wodewoeddddd',num)
            #userfile是用户文件夹下所有文件的集合
            userfile = []
            for i in range(0, num):
                temp = temp2.split('\n', 1)[0]
                userfile.append(temp)
                temp2 = temp2.split('\n', 1)[1]
            print('bbbbbbb' , userfile)
            #list2是用户文件夹下的所有的作业号
            all_job_num = re.findall('[0-9][0-9]{5}', result)
            print('cccccc' , all_job_num)
            #用于存放每个文件的大小
            size = []
            #用于存放正在运行的作业在所有作业中的编号
            array1 = []
            #result用于存放处理好的数据
            result = []
            for i in range(0, len(now_job_num)):
                if (all_job_num.index(now_job_num[i]) != -1):
                    array1.append(all_job_num.index(now_job_num[i]))

            #获得这些作业的大小，并放到size中
            for i in range(0, len(array1)):
                temp = userfile[array1[i]]
                d = 'cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/' + temp + ';ls -l |grep "^-"|wc -l'
                stdin, stdout, stderr = ssh.exec_command(d)
                d = stdout.read()
                d = d.decode()
                d = d.split('\n', 1)[0]
                d = d + 'K'
                print('每个多大')
                print(d)
                size.append(d)
            print('sunbo')
            print(size)
            for i in range(0, len(array1)):
                temp = userfile[array1[i]]
                task_id = temp.split('-s', 1)[0]
                temp = temp.split('-', 2)[2]
                materialid1 = temp.split('-', 1)[0]
                materialid2 = temp.split('-', 2)[1]
                materialid = materialid1 + '-' + materialid2
                prettyformula = temp.split('-', 3)[2]
                thissize = size[i]
                string = {'taskid': task_id, 'slid': materialid, 'prettyformula': prettyformula, 'size': thissize}
                result.append(string)
            #final_result是传递给前台的数据
            final_result = list(result)
            print('数据如下')
            print(final_result)
            data = json_util.dumps(final_result)
            print('最后一步了大哥')
            return JsonResponse(data, safe=False)
        else:
            return render(request, 'taskmanage.html',{'username':username,'email':email})
    else:
        return redirect("/door/")
#完成任务的界面
@csrf_exempt
def taskmanage_completed(request):
    print('进入到了完成界面'
          )
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        if request.is_ajax():
            #与服务器建立连接
            ssh = paramiko.SSHClient()
            policy = paramiko.AutoAddPolicy()
            ssh.set_missing_host_key_policy(policy)
            ssh.connect(
                hostname="172.26.18.243",  # 服务器的ip
                port=22,  # 服务器的端口
                username="gromacs",  # 服务器的用户名
                password="gromacs"  # 用户名对应的密码
            )
            #linux命令，分别获得bjobs的结果，用户所有的文件名
            c = 'cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/;ls'
            stdin, stdout, stderr = ssh.exec_command(c)
            a = stdout.read()
            b = a.decode()
            result = b
            num = b.count('\n')
            array = []
            transform_result=[]
            resultarray = []
            for i in range(0, num):
                temp = b.split('\n', 1)[0]
                array.append(temp)
                b = b.split('\n', 1)[1]
            for i in range(0, num):
                temp = 'cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/' + array[i] + ';ls'
                stdin, stdout, stderr = ssh.exec_command(temp)
                temp = stdout.read()
                temp = temp.decode()
                tempnum = temp.count('\n')
                temparray = []
                for m in range(0, tempnum):
                    other = temp.split('\n', 1)[0]
                    temparray.append(other)
                    temp = temp.split('\n', 1)[1]
                mnt = 0
                for n in range(0, tempnum):
                    error = temparray[n].find('err')
                    out = temparray[n].find('out')
                    if (error != -1 or out != -1):
                        mnt = mnt + 1

                if (mnt == 2):
                    resultarray.append(array[i])
            size = []
            for i in range(0, len(resultarray)):
                temp = resultarray[i]
                d = 'cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/' + temp + ';ls -l |grep "^-"|wc -l'
                stdin, stdout, stderr = ssh.exec_command(d)
                d = stdout.read()
                d = d.decode()
                d = d.split('\n', 1)[0]
                d = d + 'K'
                size.append(d)
            for i in range(0, len(resultarray)):
                temp = resultarray[i]

                task_id = temp.split('-s', 1)[0]

                temp = temp.split('-', 2)[2]
                materialid1 = temp.split('-', 1)[0]
                materialid2 = temp.split('-', 2)[1]
                materialid = materialid1 + '-' + materialid2
                prettyformula = temp.split('-', 3)[2]
                thissize = size[i]
                string = {'taskid': task_id, 'slid': materialid, 'prettyformula': prettyformula, 'size': thissize}
                transform_result.append(string)
            #final_result是传递给前台的数据
            final_result = list(transform_result)
            print('数据如下')
            print(final_result)
            data = json_util.dumps(final_result)
            print('最后一步了大哥')
            return JsonResponse(data, safe=False)
        else:
            return render(request, 'taskmanage.html',{'username':username,'email':email})
    else:
        return redirect("/door/")
#用户退出登录的功能
def logout(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        servername = request.session.get('SERVERNAME', False)
        serverpassword = request.session.get('SERVERPASSWORD', False)
        del request.session['USRNAME']
        del request.session['EMAIL']
        del request.session['IS_LOGIN']
        if(servername!=False and serverpassword!=False):
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
#材料具体信息
def materialdetail(request):
    slid = request.GET.get('slid')
    print(slid)
    contact_list = Material.matobj.filter(slid=slid)
    paginator = Paginator(contact_list, 10)
    contacts = paginator.get_page('1')
    print('begin')
    print(contacts)
    return render(request, "structure.html", {'contacts': contacts})
#her体系，目前还没有实际用处
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
#机器学习SVC方法
@csrf_exempt
def svc(request):
    if request.method == 'POST':
        time1 = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        username = request.session.get('USRNAME', False)
        csv_file = request.FILES.get("file")
        task_name=request.POST.get('task_name')
        print(task_name)
        c = float(request.POST.get('C'))
        degree = float(request.POST.get('degree'))
        gamma = float(request.POST.get('gamma'))
        coef0 = float(request.POST.get('coef0'))
        max_itera = float(request.POST.get('max_iter'))
        middle=pd.read_csv(csv_file)
        middle.to_csv('middle.csv',index=False,encoding="UTF8")
        print('成功了吗')
        address = './User/' + username + '-ml/' + task_name
        csvadress = './User/' + username + '-ml/' + task_name + '/resultnew.csv'
        os.mkdir(address)
#代码融合开始
        with open("middle.csv", "r", encoding="utf-8") as vsvfile:
            reader = csv.reader(vsvfile)
            rows = [row for row in reader]
        # array1是元素的列名，array2是元素所在的列号,rows表示有多少行（算上了表头）一个元素会增加59个额外特征
        array1 = []
        array2 = []
        print(len(rows))
        for i in range(0, len(rows[0])):
            if rows[0][i].startswith('element'):
                array1.append(rows[0][i])
                array2.append(i)
        if len(array2) == 0:
            middle.to_csv(csvadress, index=False, encoding="UTF8")
        else:
            num_feature_original = (len(rows[0]) - len(array1) - 3)
            num_feature_change = num_feature_original + 59 * len(array1)
            print(num_feature_original, num_feature_change)
            # --------------------------------------------获得基本数据结束----------------------------------
            # 读取数据表
            aFile = open('middle.csv', 'r')
            aInfo = csv.reader(aFile)
            bfile = open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\elements.csv', 'r')
            bInfo = csv.reader(bfile)
            # 构造结果csv文件
            cfile = open('result.csv', 'w', newline="")
            abcsv = csv.writer(cfile, dialect='excel')
            a = list()
            # c做一个备份
            c = a
            b = list()
            for info in aInfo:
                a.append(info)
            for info in bInfo:
                b.append(info)
            # 将elements表格去掉前两列
            b = list(map(lambda x: x[2:], b))
            for index in range(len(a)):
                for i in range(len(array1)):
                    if index == 0:
                        c[index].extend(b[index])
                    else:
                        c[index].extend(b[int(a[index][array2[i]])])
                abcsv.writerow(c[index])
            # ---------------------------------------------拼接完成-------------------------------------
            # --------------------------------对拼接完的表格进行完善------------------------------------
            resultnum = list()
            aFile = open('result.csv', 'r')
            aInfo = csv.reader(aFile)
            for info in aInfo:
                resultnum.append(info)

            print('lalalala')
            print(csvadress)
            cfile = open(csvadress, 'w', newline="")
            colname1 = []
            colname2 = []
            for i in range(num_feature_original, num_feature_change):
                colname1.append('a' + str(i + 1))
            for i in range(num_feature_original):
                colname2.append('a' + str(i + 1))
            colname = ['NO', 'Class', 'Target'] + colname2 + colname1
            print(colname)
            abcsv = csv.writer(cfile, dialect='excel')
            for index in range(0, len(resultnum)):
                print(index)
                if index == 0:
                    resultnum[index] = (colname)
                else:
                    num = array2[1] - 1
                    for i in array2:
                        del resultnum[index][num]
                        # resultnum[index]=resultnum[index].remove(resultnum[index][num])
                abcsv.writerow(resultnum[index])
            cfile.close()
        #代码融合结束

        #机器学习代码开始
        df = pd.read_csv(r'./User/'+username+'-ml/'+task_name+'/resultnew.csv', index_col=0)
        columns = df.columns.values.tolist()
        col_target = []
        col_Class = []
        col_feature = []
        for i in columns:
            if i == 'Class':
                col_Class.append(i)
            else:
                if i == 'Target':
                    col_target.append(i)
                else:
                    col_feature.append(i)
        df_target = df[col_target]
        df_feature = df[col_feature]
        df_class = df[col_Class]
        # model = SVC(kernel='linear')#线性可分
        model = SVC(kernel='rbf', C=c, gamma=gamma, degree=degree, coef0=coef0, max_iter=max_itera)
        model.fit(df_feature, df_class)

        modelname='./User/'+username+'-ml/'+task_name+'/'+task_name+'.model'
        starttime='./User/'+username+'-ml/'+task_name+'/starttime.txt'
        endtime = './User/' + username + '-ml/' + task_name + '/endtime.txt'
        print(modelname)
        joblib.dump(filename=modelname, value=model)
        time2 = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        with open(starttime, 'wb') as destination:
            time1=time1.encode()
            destination.write(time1)
        destination.close()
        with open(endtime, 'wb') as destination:
            time2=time2.encode()
            destination.write(time2)
        destination.close()
        data = '1'
        return JsonResponse(data, safe=False)
    else:
        return render(request, "svc.html")
#机器学习SVC方法
@csrf_exempt
def linear(request):
    if request.method == 'POST':
        time1 = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        username = request.session.get('USRNAME', False)
        csv_file = request.FILES.get("file")
        task_name=request.POST.get('task_name')
        eta = float(request.POST.get('eta'))
        middle=pd.read_csv(csv_file)
        middle.to_csv('middle.csv',index=False,encoding="UTF8")
        print('成功了吗')
        address = './User/' + username + '-ml/' + task_name
        csvadress = './User/' + username + '-ml/' + task_name + '/resultnew.csv'
        os.mkdir(address)
#代码融合开始
        with open("middle.csv", "r", encoding="utf-8") as vsvfile:
            reader = csv.reader(vsvfile)
            rows = [row for row in reader]
        # array1是元素的列名，array2是元素所在的列号,rows表示有多少行（算上了表头）一个元素会增加59个额外特征
        array1 = []
        array2 = []
        print(len(rows))
        for i in range(0, len(rows[0])):
            if rows[0][i].startswith('element'):
                array1.append(rows[0][i])
                array2.append(i)
        if len(array2) == 0:
            middle.to_csv(csvadress, index=False, encoding="UTF8")
        else:
            num_feature_original = (len(rows[0]) - len(array1) - 3)
            num_feature_change = num_feature_original + 59 * len(array1)
            print(num_feature_original, num_feature_change)
            # --------------------------------------------获得基本数据结束----------------------------------
            # 读取数据表
            aFile = open('middle.csv', 'r')
            aInfo = csv.reader(aFile)
            bfile = open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\elements.csv', 'r')
            bInfo = csv.reader(bfile)
            # 构造结果csv文件
            cfile = open('result.csv', 'w', newline="")
            abcsv = csv.writer(cfile, dialect='excel')
            a = list()
            # c做一个备份
            c = a
            b = list()
            for info in aInfo:
                a.append(info)
            for info in bInfo:
                b.append(info)
            # 将elements表格去掉前两列
            b = list(map(lambda x: x[2:], b))
            for index in range(len(a)):
                for i in range(len(array1)):
                    if index == 0:
                        c[index].extend(b[index])
                    else:
                        c[index].extend(b[int(a[index][array2[i]])])
                abcsv.writerow(c[index])
            # ---------------------------------------------拼接完成-------------------------------------
            # --------------------------------对拼接完的表格进行完善------------------------------------
            resultnum = list()
            aFile = open('result.csv', 'r')
            aInfo = csv.reader(aFile)
            for info in aInfo:
                resultnum.append(info)

            print('lalalala')
            print(csvadress)
            cfile = open(csvadress, 'w', newline="")
            colname1 = []
            colname2 = []
            for i in range(num_feature_original, num_feature_change):
                colname1.append('a' + str(i + 1))
            for i in range(num_feature_original):
                colname2.append('a' + str(i + 1))
            colname = ['NO', 'Class', 'Target'] + colname2 + colname1
            print(colname)
            abcsv = csv.writer(cfile, dialect='excel')
            for index in range(0, len(resultnum)):
                print(index)
                if index == 0:
                    resultnum[index] = (colname)
                else:
                    num = array2[1] - 1
                    for i in array2:
                        del resultnum[index][num]
                        # resultnum[index]=resultnum[index].remove(resultnum[index][num])
                abcsv.writerow(resultnum[index])
            cfile.close()
        #代码融合结束

        #机器学习代码开始
        df = pd.read_csv(r'./User/'+username+'-ml/'+task_name+'/resultnew.csv', index_col=0)
        columns = df.columns.values.tolist()
        col_target = []
        col_Class = []
        col_feature = []
        for i in columns:
            if i == 'Class':
                col_Class.append(i)
            else:
                if i == 'Target':
                    col_target.append(i)
                else:
                    col_feature.append(i)
        df_target = df[col_target]
        df_feature = df[col_feature]
        df_target = df_target['Target']
        df_class = df[col_Class]
        # model = SVC(kernel='linear')#线性可分
        reg = linearR()
        reg.fit_gd(df_feature, df_target, eta=eta)

        modelname='./User/'+username+'-ml/'+task_name+'/'+task_name+'.model'
        print('lalalalal')
        print(modelname)
        starttime='./User/'+username+'-ml/'+task_name+'/starttime.txt'
        endtime = './User/' + username + '-ml/' + task_name + '/endtime.txt'
        print(modelname)
        joblib.dump(filename=modelname, value=reg)
        time2 = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        time2 = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        with open(starttime, 'wb') as destination:
            time1=time1.encode()
            destination.write(time1)
        destination.close()
        with open(endtime, 'wb') as destination:
            time2=time2.encode()
            destination.write(time2)
        destination.close()
        data = '1'
        return JsonResponse(data, safe=False)
    else:
        return render(request, "linear.html")
#机器学习DTC方法
def dtc(request):
    if request.method == 'POST':
        min_impurity_decrease = int(request.POST.get('min_impurity_decrease'))
        min_samples_leaf = int(request.POST.get('min_samples_leaf'))
        min_samples_split = int(request.POST.get('min_samples_split'))
        max_depth = int(request.POST.get('max_depth'))
        random_state = int(request.POST.get('random_state'))
        # 机器学习代码开始
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
#机器学习PCA方法
def pca(request):
    if request.method == 'POST':
        #机器学习代码开始
        wine = load_wine()
        X = wine.data
        y = wine.target
        # print(y.shape)
        # print(pd.DataFrame(y))
        pca = PCA(
            n_components='mle'  # 最大似然估计，自动选择降维后的特征个数
            , copy=True
            , whiten=False
            , )  # 默认为原特征数量
        X_dr = pca.fit_transform(X)
        # print(X_dr)
        # X_dr[y == 0, 0]
        # plt.figure()
        # plt.scatter(X_dr[y==0, 0], X_dr[y==0, 1], c="red", label=wine.target_names[0])
        # plt.scatter(X_dr[y==1, 0], X_dr[y==1, 1], c="black", label=wine.target_names[1])
        # plt.scatter(X_dr[y==2, 0], X_dr[y==2, 1], c="orange", label=wine.target_names[2])
        # plt.legend()
        # plt.title('PCA of wine dataset')
        # plt.show()
        colors = ['red', 'black', 'orange']
        plt.figure()
        for i in [0, 1, 2]:
            plt.scatter(X_dr[y == i, 0]
                        , X_dr[y == i, 1]
                        , alpha=.7
                        , c=colors[i]
                        , label=wine.target_names[i]
                        )
        plt.legend()
        plt.title('PCA of wine dataset')
        print(pca.explained_variance_)  # 降维后每个特征所带的信息量
        print(pca.explained_variance_ratio_)  # 降维后每个特征的信息量占总信息量的百分比（方差贡献率）
        print(pca.explained_variance_ratio_.sum())  # 降维后所有特征信息量占总信息量的百分比
        # 累积可解释方差贡献率曲线
        # 累积可解释方差贡献率曲线是一条以降维后保留的特征个数为横坐标，降维后新特征矩阵捕捉到的可解释方差贡献
        # 率为纵坐标的曲线，能够帮助我们决定n_components最好的取值。
        plt.plot([1, 2, 3, 4, 5, 6], np.cumsum(pca.explained_variance_ratio_))
        plt.xticks([1, 2, 3, 4, 5, 6])  # 这是为了限制坐标轴显示为整数
        plt.xlabel("number of components after dimension reduction")
        plt.ylabel("cumulative explained variance")
        plt.savefig('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\static\\css\\picture\\comment2.png')
        return render(request, "result2.html")
    else:
        return render(request, "pca.html")

def pearson(request):
    if request.method == 'POST':
        csv_file = request.FILES.get("files")
        print(csv_file)
        middle=pd.read_csv(csv_file)
        middle.to_csv('middle.csv',index=False,encoding="UTF8")
#代码融合开始
        with open("middle.csv", "r", encoding="utf-8") as vsvfile:
            reader = csv.reader(vsvfile)
            rows = [row for row in reader]
        # array1是元素的列名，array2是元素所在的列号,rows表示有多少行（算上了表头）一个元素会增加59个额外特征
        array1 = []
        array2 = []
        print(len(rows))
        for i in range(0, len(rows[0])):
            if rows[0][i].startswith('element'):
                array1.append(rows[0][i])
                array2.append(i)
        if len(array2) == 0:
            middle = pd.read_csv(csv_file)
            middle.to_csv('resultnew.csv', index=False, encoding="UTF8")
        else:
            num_feature_original = (len(rows[0]) - len(array1) - 3)
            num_feature_change = num_feature_original + 59 * len(array1)
            print(num_feature_original, num_feature_change)
            # --------------------------------------------获得基本数据结束----------------------------------
            # 读取数据表
            aFile = open('middle.csv', 'r')
            aInfo = csv.reader(aFile)
            bfile = open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\elements.csv', 'r')
            bInfo = csv.reader(bfile)
            # 构造结果csv文件
            cfile = open('result.csv', 'w', newline="")
            abcsv = csv.writer(cfile, dialect='excel')
            a = list()
            # c做一个备份
            c = a
            b = list()
            for info in aInfo:
                a.append(info)
            for info in bInfo:
                b.append(info)
            # 将elements表格去掉前两列
            b = list(map(lambda x: x[2:], b))
            for index in range(len(a)):
                for i in range(len(array1)):
                    if index == 0:
                        c[index].extend(b[index])
                    else:
                        c[index].extend(b[int(a[index][array2[i]])])
                abcsv.writerow(c[index])
            # ---------------------------------------------拼接完成-------------------------------------
            # --------------------------------对拼接完的表格进行完善------------------------------------
            resultnum = list()
            aFile = open('result.csv', 'r')
            aInfo = csv.reader(aFile)
            for info in aInfo:
                resultnum.append(info)
            print('aaaaa')
            cfile = open('resultnew.csv', 'w', newline="")
            colname1 = []
            colname2 = []
            print('lalalalala')
            print(num_feature_original,num_feature_change)
            for i in range(num_feature_original, num_feature_change):
                colname1.append('a' + str(i + 1))
            for i in range(num_feature_original):
                colname2.append('a' + str(i + 1))
            print(colname1)
            print(colname2)
            colname = ['NO', 'Class', 'Target'] + colname2 + colname1
            print(colname)
            abcsv = csv.writer(cfile, dialect='excel')
            for index in range(0, len(resultnum)):
                print(index)
                if index == 0:
                    resultnum[index] = (colname)
                else:
                    num = array2[1] - 1
                    for i in array2:
                        del resultnum[index][num]
                        # resultnum[index]=resultnum[index].remove(resultnum[index][num])
                abcsv.writerow(resultnum[index])
            cfile.close()
        #代码融合结束
        #机器学习代码开始
        df = pd.read_csv('resultnew.csv', header=[0,1,2])
        df.corr()  # 计算pearson相关系数
        dfData = df.corr()
        plt.subplots(figsize=(26, 26))  # 设置画面大小
        sns.heatmap(dfData, annot=True, vmax=1, square=True, cmap="Blues")
        plt.savefig('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\static\\css\\picture\\comment3.png')
        return render(request, "result3.html")
    else:
        return render(request, "pearson.html")
#高通量选择物质之后的跳转模块
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
#高通量模块
@csrf_exempt
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
#网站教程模块
def tutorials(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        return render(request, 'maps.html',{'username': username,'email':email})
    else:
        return redirect("/door/")
#提供VASP任务下载模块
def downloads(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        #文件处理部分
        taskid = request.GET.get('taskid')
        ssh = paramiko.SSHClient()
        policy = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(policy)
        ssh.connect(
            hostname="172.26.18.243",  # 服务器的ip
            port=22,  # 服务器的端口
            username="gromacs",  # 服务器的用户名
            password="gromacs"  # 用户名对应的密码
        )
        c = 'cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/;ls'
        # 查询bjobs的结果
        stdin, stdout, stderr = ssh.exec_command(c)
        a = stdout.read()
        b = a.decode()
        num = b.count('\n')
        array = []
        for i in range(0, num):
            temp = b.split('\n', 1)[0]
            array.append(temp)
            b = b.split('\n', 1)[1]
        for i in range(0,num):
            if array[i].startswith(taskid):
                filename=array[i]
        tarfilename=taskid+'.tar.gz'
        d = 'cd /gpfs/home/gromacs/BM/User/xiaoxiaobo/;'+'tar -cvzf   '+tarfilename+' '+filename
        stdin, stdout, stderr = ssh.exec_command(d)
        #file=刚才压缩的文件名
        socket.setdefaulttimeout(20)
        username = request.session.get('USRNAME', False)
        email = request.session.get('EMAIL', False)
        taskid = request.GET.get('taskid')
        file = open('/bm_project/static/test.xlsx', 'rb')
        response = FileResponse(open('/bm_project/static/test.xlsx', 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="test.xlsx"'
        print(response.items())
        time.sleep(1)
        return response
        response.close()
    else:
        return redirect("/door/")

def mlmanage(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    dir='./User/'+username+'-ml'
    list = os.listdir(dir)
    filenum=len(list)
    print(filenum)
    #子目录名字
    child_filename_array=[]
    for i in range(0,filenum):
        child_filename_array.append('./User/'+username+'-ml'+'/'+list[i])
    starttime_array=[]
    endtime_array=[]
    for i in range(0,filenum):
        temp_starttime_file=child_filename_array[i]+'/starttime.txt'
        temp_endtime_file=child_filename_array[i]+'/endtime.txt'
        with open(temp_starttime_file,'r') as f:
            starttime_array.append(f.read())
        with open(temp_endtime_file,'r') as f:
            endtime_array.append(f.read())
    resultarray=[]
    for i in range(0,filenum):
        temp_result={'num':i,'starttime':starttime_array[i],'endtime':endtime_array[i],'task_name':list[i]}
        resultarray.append(temp_result)
    print(type(resultarray))
    paginator = Paginator(resultarray, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, "mlmanage.html", {'contacts': contacts,'username': username, 'email': email})

def ready_topredict(request):
    username = request.session.get('USRNAME', False)
    email = request.session.get('EMAIL', False)
    task_name = request.GET.get('task_name')
    dir = './User/' + username + '-ml'+'/'+task_name
    list = os.listdir(dir)
    filenum = len(list)
    marker=0
    for i in range(0,filenum):
        name='model'
        if(name in list[i]):
            marker=1
    #如果没有保存的模型，那么就是预测的任务，marker=0,；如果是训练的模型，那么marker=1
    print('lalalal')
    print(marker)
    if(marker==1):
        #实例写几个评价指标，目前是用开始与结束时间作为两个评价指标
        starttime_address=dir+'/starttime.txt'
        endtime_address = dir + '/endtime.txt'
        with open(starttime_address,'r') as f:
            starttime=f.read()
        with open(endtime_address,'r') as f:
            endtime=f.read()
        resultarray = {'starttime':starttime,'endtime':endtime,'marker':marker,'task_name':task_name}
        return render(request, "readytopredict.html", {'contacts': resultarray,'username': username, 'email': email})
    else:
        starttime_address = dir + '/starttime.txt'
        endtime_address = dir + '/endtime.txt'
        with open(starttime_address,'r') as f:
            starttime=f.read()
        with open(endtime_address,'r') as f:
            endtime=f.read()
        resultarray = {'starttime': starttime, 'endtime': endtime, 'marker': marker, 'task_name': task_name}
        return render(request, "predictresult.html", { 'contacts': resultarray,'username': username, 'email': email})
def predict(request):
    if request.method == 'POST':
        time1 = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        username = request.session.get('USRNAME', False)
        csv_file = request.FILES.get("file")
        task_name = request.POST.get('task_name')
        task_name_old = request.POST.get('task_name_old')
        middle = pd.read_csv(csv_file)
        middle.to_csv('middle.csv', index=False, encoding="UTF8")
        print('成功了吗')
        # 代码融合开始
        with open("middle.csv", "r", encoding="utf-8") as vsvfile:
            reader = csv.reader(vsvfile)
            rows = [row for row in reader]
        # array1是元素的列名，array2是元素所在的列号,rows表示有多少行（算上了表头）一个元素会增加59个额外特征
        array1 = []
        array2 = []
        print(len(rows))
        for i in range(0, len(rows[0])):
            if rows[0][i].startswith('element'):
                array1.append(rows[0][i])
                array2.append(i)
        if len(array2) == 0:
            middle.to_csv('resultnew.csv', index=False, encoding="UTF8")
        else:
            num_feature_original = (len(rows[0]) - len(array1) - 3)
            num_feature_change = num_feature_original + 59 * len(array1)
            print(num_feature_original, num_feature_change)
            # --------------------------------------------获得基本数据结束----------------------------------
            # 读取数据表
            aFile = open('middle.csv', 'r')
            aInfo = csv.reader(aFile)
            bfile = open('C:\\Users\\xiaoxiaobo123\\PycharmProjects\\BM_Project\\bm_project\\elements.csv', 'r')
            bInfo = csv.reader(bfile)
            # 构造结果csv文件
            cfile = open('result.csv', 'w', newline="")
            abcsv = csv.writer(cfile, dialect='excel')
            a = list()
            # c做一个备份
            c = a
            b = list()
            for info in aInfo:
                a.append(info)
            for info in bInfo:
                b.append(info)
            # 将elements表格去掉前两列
            b = list(map(lambda x: x[2:], b))
            for index in range(len(a)):
                for i in range(len(array1)):
                    if index == 0:
                        c[index].extend(b[index])
                    else:
                        c[index].extend(b[int(a[index][array2[i]])])
                abcsv.writerow(c[index])
            # ---------------------------------------------拼接完成-------------------------------------
            # --------------------------------对拼接完的表格进行完善------------------------------------
            resultnum = list()
            aFile = open('result.csv', 'r')
            aInfo = csv.reader(aFile)
            for info in aInfo:
                resultnum.append(info)
            print('aaaaa')
            cfile = open('resultnew.csv', 'w', newline="")
            colname1 = []
            colname2 = []
            for i in range(num_feature_original, num_feature_change):
                colname1.append('a' + str(i + 1))
            for i in range(num_feature_original):
                colname2.append('a' + str(i + 1))
            colname = ['NO', 'Class', 'Target'] + colname2 + colname1
            print(colname)
            abcsv = csv.writer(cfile, dialect='excel')
            for index in range(0, len(resultnum)):
                print(index)
                if index == 0:
                    resultnum[index] = (colname)
                else:
                    num = array2[1] - 1
                    for i in array2:
                        del resultnum[index][num]
                        # resultnum[index]=resultnum[index].remove(resultnum[index][num])
                abcsv.writerow(resultnum[index])
            cfile.close()
        # 代码融合结束

        # 机器学习代码开始
        model_address=dir = './User/' + username + '-ml'+'/'+task_name_old+'/'+task_name_old+'.model'
        model1 = joblib.load(filename=model_address)
        #获得特征
        df = pd.read_csv(r'resultnew.csv', index_col=0)
        columns = df.columns.values.tolist()
        col_target = []
        col_Class = []
        col_feature = []
        for i in columns:
            if i == 'Class':
                col_Class.append(i)
            else:
                if i == 'Target':
                    col_target.append(i)
                else:
                    col_feature.append(i)
        df_target = df[col_target]
        df_feature = df[col_feature]
        predict_result=model1.predict(df_feature)
        df = DataFrame(predict_result, columns=['Target'])
        result = pd.concat([df_feature, df], axis=1)
        result_address = './User/' + username + '-ml/' + task_name + '/resultnew.csv'
        address = './User/' + username + '-ml/' + task_name
        os.mkdir(address)
        starttime = './User/' + username + '-ml/' + task_name + '/starttime.txt'
        endtime = './User/' + username + '-ml/' + task_name + '/endtime.txt'
        time2 = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        with open(starttime, 'wb') as destination:
            time1 = time1.encode()
            destination.write(time1)
        destination.close()
        with open(endtime, 'wb') as destination:
            time2 = time2.encode()
            destination.write(time2)
        destination.close()
        result.to_csv(result_address)
        data = '1'
        return JsonResponse(data, safe=False)
    else:
        task_name_old = request.GET.get('task_name_old')
        result = {'task_name_old': task_name_old}
        return render(request, "predict.html",{ 'contacts': result})

def data_download(request):
    username = request.session.get('USRNAME', False)
    task_name_old=request.GET.get('task_name_old')
    print(task_name_old)
    data_adress='./User/' + username + '-ml/' + task_name_old + '/resultnew.csv'
    response = FileResponse(open(data_adress, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="resultnew.csv"'
    return response











