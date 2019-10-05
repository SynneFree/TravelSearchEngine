from django.conf import settings
from myapp import myAPI
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
from myapp.models import *
from myapp.forms import *
from django.db.models import Q
import json
import datetime
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from elasticsearch import Elasticsearch



# Create your views here.
es = Elasticsearch()
G_dir=settings.JSON_ROOT+'location.json'


def index(request):
    request.session.set_expiry(0)
    request.session['collected']=False
    data=myAPI.load_data(G_dir)
    return render(request,'html/home2.html',locals())

def register(request):
    username = request.POST['register_username']
    password = request.POST['register_password']
    email = request.POST['register_email']
    msg = ''
    print(username)
    user_exist=User.objects.filter(pk=username)
    if user_exist:
        return HttpResponse("该用户已存在")
    new_user=User(
        username=username,
        email=email,
        password=password,
    )
    new_user.save()
    msg='注册成功'
    return redirect('/login')

def login(request):
    data = myAPI.load_data(G_dir)
    if request.session.get('is_login', None):
        return redirect('/')
    if request.method == "POST":
        username=request.POST['login_username']
        password=request.POST['login_password']
        checkpass=User.objects.filter(username__exact=username,password__exact=password)
        if checkpass:
            request.session['is_login'] = True
            request.session['user_name'] = username
            print("login success")
            return redirect('/home',locals())
        else:
            message='用户不存在或密码错误!'
            return HttpResponse(message)
    return render(request, 'html/login2.html', locals())

def logout(request):
    del request.session['is_login']
    del request.session['user_name']
    request.session['is_login'] = False
    return redirect('/')

def personal_center(request):
    if not request.session.get('is_login'):
        return redirect('/login')
    hot_list=Hot_attraction.objects.all().order_by('hot_rank')[:4]
    Attraction_list = []
    for item in hot_list:
        attractionName=item.attraction_name
        #print(attractionName)
        Attraction=myAPI.search_by_name_exactly(attractionName)
        #print('test:'+str(Attraction))
        if Attraction:
            Attraction_list.append(Attraction)
    context={
        'hot_list':Attraction_list,
    }
    return render(request,'html/personal_center.html',context)

def test_add(request):
    if request.is_ajax():
        print("ajax请求")
        a = request.POST['a']
        b = request.POST['b']
        a = int(a)
        b = int(b)
        return JsonResponse(str(a + b),safe=False)
    return render(request,'html/test.html')


def page_test(request):
    List=[i for i in range(120)]
    paginator=Paginator(List,12)
    page=request.GET.get('page',1)
    currentPage=int(page)
    try:
        #print(page)
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request,'html/pageTest.html',locals())


def search_by_area(request):
    G_data = myAPI.load_data(G_dir)
    area_field=request.GET.get('area-field',None)
    List,Scores,msg=myAPI.search_by_area(area_field)
    paginator = Paginator(List, 12)
    page = request.GET.get('page', 1)
    try:
        #print(page)
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    context = {
        'list': list,
        'area_field':area_field,
        'searchingArea':True,
        'skipTo':0,
        'msg': msg,
        'data': G_data
    }
    return render(request, 'html/result.html', context)


def search(request):
    is_login=request.session.get('is_login',None)
    userName=request.session.get('user_name',None)
    search_field=request.GET.get('search_field',None)
    G_data = myAPI.load_data(G_dir)

    print(search_field)

    if search_field !='':
        List,Scores,msg=myAPI.search(search_field)
    else:
        List,Scores,msg=[],[],''
    for l in List:
        print(l['name']+'  '+l['location']+' '+l['feature'])
    #print(List)
    paginator=Paginator(List,12)
    page=request.GET.get('page',1)
    try:
        #print(page)
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    context={
        'list':list,
        'Scores':Scores,
        'msg':msg,
        'skipTo':1,
        'search_field':search_field,
        'data':G_data
    }
    if search_field!='' and is_login:
        is_search = Search_record.objects.filter(user_name__exact=userName, search_field__exact=search_field)
        print(bool(is_search))
        if is_search:
            is_search.update(timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            new_record=Search_record(
                user_name=userName,
                search_field=search_field,
                timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            new_record.save()
    return render(request,'html/result.html',context)

def attraction_detail(request):
    name = request.GET.get('attractionName', None)
    location = request.GET.get('attractionLocation', None)
    #List, Scores = myAPI.search_by_name_location(name)

    attraction=myAPI.search_by_name_exactly(name)
    G_data = myAPI.load_data(G_dir)
    collected=False;
    if request.session.get('is_login'):
        username=request.session.get('user_name')
        records=Collect.objects.filter(user_name__exact=username,attraction_name__exact=name)
        if records:
            collected=True
    pinyin=''
    # if List['0']['city']:
    #     pinyin = myAPI.getPinyin(List[0]['city'])
    # print(pinyin)
    # pictures=List[0]['picture']
    if attraction['city']:
        pinyin = myAPI.getPinyin(attraction['city'])
    print(pinyin)
    pictures=attraction['picture']
    print(pictures)
   # pictures=json.loads(pictures)
    context = {
        'Attraction': attraction,
        'collected':collected,
        'pictures':pictures,
        'pinyin':pinyin,
        'data': G_data
    }
    #print(pictures)
    return render(request, 'html/attraction.html', context)

def cancel_collect(request):
    if request.is_ajax():
        userName=request.POST.get('userName',)
        attractionName=request.POST.get('attractionName','')
        location = request.POST.get('location', '')
        check = Collect.objects.filter(user_name__exact=userName,
                                       attraction_name__exact=attractionName,
                                       location__exact=location)
        if check:
            check.delete()
            attraction=Hot_attraction.objects.get(
                attraction_name__exact=attractionName,
                location__exact=location
            )
            attraction.hot_rank=attraction.hot_rank-1;
            if attraction.hot_rank<1:
                attraction.delete()
            else:
                attraction.save()
            isDelete=True
        else:
            isDelete=False
        return JsonResponse(isDelete, safe=False)
    return redirect('/attraction-detail')
def collect(request):
    if request.is_ajax():
        print("ajax请求")
        userName = request.POST.get('userName','')
        attractionName=request.POST.get('attractionName','')
        location = request.POST.get('location', '')
        print(userName)
        isCollect=False
        check=Collect.objects.filter(user_name__exact=userName,
                                     attraction_name__exact=attractionName,
                                     location__exact=location)
        if check:
            isCollect=True
        else:
            new_collect=Collect(
                user_name=userName,
                attraction_name=attractionName,
                location=location,
            )
            new_collect.save()
            try:
                hot = Hot_attraction.objects.get(attraction_name__exact=attractionName)
                hot.hot_rank = hot.hot_rank + 1
                hot.save()

            except Hot_attraction.DoesNotExist:
                new_hot_attraction=Hot_attraction(
                    attraction_name=attractionName,
                    location=location,
                    hot_rank=1)
                new_hot_attraction.save()
        return JsonResponse(isCollect,safe=False)
    return redirect(request,'/attraction-detail')


def check_collect(request):
    if request.is_ajax():
        userName=request.POST.get('userName','')
        print(userName)
        collects=Collect.objects.filter(user_name__exact=userName)
        Attraction_list = []
        for item in collects:
            attractionName = item.attraction_name
            print(attractionName)
            Attraction = myAPI.search_by_name_exactly(attractionName)
            # print('test:'+str(Attraction))
            if Attraction:
                Attraction_list.append(Attraction)
        ret= Attraction_list
        # ret=serializers.serialize("json",collects)
        #print(ret)
        return JsonResponse(ret,safe=False)
    return redirect(request, '/personal-center')



def check_history(request):
    if request.is_ajax():
        userName=request.POST.get('userName','')
        print(userName)
        history=Search_record.objects.filter(user_name__exact=userName).order_by('-timestamp')
        ret=serializers.serialize("json",history)
        print(ret)
        return JsonResponse(ret,safe=False)
    return redirect(request, '/personal-center')

def publish_comment(request):
    if request.is_ajax():
        flag=False
        userName = request.GET.get('userName')
        attractionName=request.GET.get('attractionName')
        comment_text = request.GET.get('comment_text')
        if userName=='':
            userName="某匿名用户"
        if comment_text=='':
            flag=False
        else:
            print(comment_text)
            new_comment=Comment(
                user_name=userName,
                attration_name=attractionName,
                comment_text=comment_text,
                timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            new_comment.save()
            flag=True
        all_comments=Comment.objects.filter(attration_name__exact=attractionName).order_by('-id')
        comment_list=serializers.serialize("json", all_comments)
        ret={
            'flag':flag,
            'comment_list':comment_list,
        }
        return JsonResponse(ret, safe=False)
    return HttpResponse("hello")

def load_comment(request):
    if request.is_ajax():
        flag=False
        attractionName=request.GET.get('attractionName')
        flag=True
        all_comments=Comment.objects.filter(attration_name__exact=attractionName).order_by('-id')
        comment_list=serializers.serialize("json", all_comments)
        ret={
            'comment_list':comment_list,
        }
        return JsonResponse(ret, safe=False)
    return HttpResponse("hello")




def check_hot(request):
    G_data = myAPI.load_data(G_dir)
    hot_list=Hot_attraction.objects.all().order_by('hot_rank')[:36]
    Attraction_list = []
    for item in hot_list:
        attractionName=item.attraction_name
        print(attractionName)
        Attraction=myAPI.search_by_name_exactly(attractionName)
        #print('test:'+str(Attraction))
        if Attraction:
            Attraction_list.append(Attraction)
    List=Attraction_list
    print(List)
    paginator = Paginator(List, 8)
    page = request.GET.get('page', 1)
    try:
        print(page)
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
         list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    context = {
        'list': list,
        'data': G_data,
        'checkingHot':True,
        'skipTo':3
    }
    return render(request,'html/result.html',context)


def check_all(request):
    G_data = myAPI.load_data(G_dir)
    List, Scores, msg = myAPI.search_all()
    paginator = Paginator(List, 12)
    page = request.GET.get('page', 1)
    try:
        print(page)
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    context = {
        'list': list,
        'Scores': Scores,
        'checkingAll':True,
        'skipTo':2,
        'msg': msg,
        'data': G_data
    }
    #print("测试")
    #print(List)
    return render(request,'html/result.html',context)