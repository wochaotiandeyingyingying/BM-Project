from pymongo import  MongoClient
import pymongo
import json
import xlrd
from requests_html import HTMLSession
from pymatgen.core.structure import Structure
session=HTMLSession()

a = xlrd.open_workbook('b.xlsx')

table = a.sheet_by_index(0) #通过索引顺序获取,0表示第一张表
m = [table.cell(i,ord('A')-ord('A')).value for i in range(4000, 5000)]
#表示将excel中含有化学id的那一栏取出，作为列表返回

for l in range(0,1000):#此处的循环变量是l，为了与之后的i相区分开来
    print(l)
    print(m[l])
    b = 'https://www.materialsproject.org/rest/v1/materials/' + m[l] + '/vasp?API_KEY=yZR7x0qJmfzkMSdp'
    c = 'https://www.materialsproject.org/rest/v1/materials/' + m[l] + '/vasp/structure?API_KEY=yZR7x0qJmfzkMSdp'
    r = session.get(b)
    strcontent=session.get(c)
    #print('cccccccc')
    content = json.loads(r.html.text)
    strcontent=json.loads((strcontent.html.text))


    #print('aaaaaaaaaaaaaaa')
    #print(content)

    #print('-----------------------------------------以下的所有代码都放在此循环中------------------------------------')



    client=MongoClient('localhost',27017)#建立MongoDB数据库连接
    mydb=client.mydb#连接所需数据库,db为数据库名
    collection=mydb.material#连接所用集合，也就是我们通常所说的表，local为表名





    strcontent=(strcontent["response"])
    strcontent=str(strcontent)
    strcontent=strcontent.split('[',1)[1]
    strcontent=strcontent.rsplit(']',1)[0]
    strcontent=strcontent.split(':',2)[2]
    strcontent=strcontent.rsplit('}',1)[0]
    strcontent = eval(strcontent)
    #structure = Structure.from_dict(b)
    #print('------------------------------------------------------structure里的数据,下来是通用数据--------------')
    #strcontent得到了数据库里存的structure的信息


    a=str(content)#str类型的
    a=str(a)
    a=a.split('[',1)[1]#str.split(s, num)[n] 参数说明： s：表示指定的分隔符，不写的话，默认是空格(’ ‘)。如果字符串中没有给定的分隔符时，则把整个字符串作为列表的一个元素返回。 num：表示分割次数。如果指定了参数num，就会将字符串分割成num+1个子字符串，并且每一个子字符串可以赋给新的变量。 [n]：表示选取第n个分片，n表示返回的list中元素下标，从0开始的。
        #a是已经去掉resonse的字符串了
    formula=a.split('pretty_formula',1)[1]
    formula=formula[4:]

    formula = formula.split('\'', 1)[0]
    #formula得到了数据库需要存的化学方程式
    #print(formula)

    ele=a.split('elements' ,1)[1]

    ele=ele[3:]

    ele=ele.split('],' ,1)[0]
    ele=ele.split("\'",1)[1]
    ele='\''+ele

    num=ele.count(',')
    total=''



    for i in range(0,num):
        temp=ele.split(',',num)[i]
        temp=temp.split('\'',1)[1]
        temp=temp.split('\'',1)[0]
        total=total+temp

    print(total)
    #total得到了数据库里存的化学元素组成

    #former=ele.split("\'",1)[0]
    #later=ele.split("\'",2)[2]
    #later=later.split("\'",1)[0]
    #complete=former+later




    #ele=eval(ele)
    #n=set(m)==set(ele)


    #print('-----------------------------------------------已经得到各个化学物质的id了，接下是怎么存储-------------------------------------------------------------------')


    #collection.insertOne({'material_id':m[l],'imformation':a})
    #m[l]也就是化学id是从excel中得到的
    data1={'materialid':m[l],'prettyformula':formula,'elements':total,'structure':strcontent,'imformation':a}
    mydb.material.insert_one(data1)
    #print('-----------------------------------------------已经可以通过循环的方式进行存储，需要注意的是存储语句不能每次运行都跑存储语句，因为没有查重，跑一次会加一个记录，不用时需注释掉---------------------------------------------------------------')
    #db.local.remove()

    #for item in collection.find({},{'elements':1}):
    #     item=item['elements']
    #     print(type(item))
    #     a=['Cr','Li']
    #     item=eval(item)
    #     b=set(a)==set(item)
    #     print(b)
    #for item in collection.find():

    #
    #
     #   print(item)







