from django.conf import settings
from myapp import myAPI
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
from myapp.models import *
from myapp.forms import *
from django.db.models import Q
import json
from elasticsearch import Elasticsearch
# Create your views here.
es = Elasticsearch()
G_dir=settings.JSON_ROOT+'location.json'


def index2(request):
    data=myAPI.load_data(G_dir)
    if request.is_ajax():
        print("前端发起ajax请求---get-city")
        province=request.GET['province']
        CITY=[]
        for item in data:
            if item['name']==province:
                cityList=item['cityList']
                for city in cityList:
                    CITY.append(city['name'])
                break
        print(CITY)
        print(province)
        #ret=data[]
        ret=CITY
        print(json.dumps(ret))
        return HttpResponse(json.dumps(ret))
    context={
        'data':data
    }
    return render(request,'html/home2.html',context)

def get_area(request):
    data=myAPI.load_data(G_dir)
    if request.is_ajax():
        print("前端发起ajax请求---get-area")
        current_province = request.GET['currentProvince']
        city = request.GET['city']
        AREA=[]
        for p in data:
            if p['name']==current_province:
                cityList=p['cityList']
                for c in cityList:
                    if c['name']==city:
                        areaList=c['areaList']
                        for a in areaList:
                            AREA.append(a['name'])
        print(AREA)
        #ret=data[]
        ret=AREA
        return HttpResponse(json.dumps(ret))
    context={
        'data':data
    }
    return render(request,'html/home.html',context)



def get_city(request):
    data=myAPI.load_data(G_dir)
    if request.is_ajax():
        print("前端发起ajax请求---get-city")
        province=request.GET['province']
        CITY=[]
        for item in data:
            if item['name']==province:
                cityList=item['cityList']
                for city in cityList:
                    CITY.append(city['name'])
                break
        print(CITY)
        print(province)
        #ret=data[]
        ret=CITY
        print(json.dumps(ret))
        return HttpResponse(json.dumps(ret))
    context={
        'data':data
    }
    return render(request,'html/home.html',context)

def unfold(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return redirect('/test',name_dict)
    #return JsonResponse(name_dict)


def test(request):
    if request.is_ajax():
        print("前端发起ajax请求")
        print(request.body)
        ret={
            'msg':'AJAX测试'
        }
        print(json.dumps(ret))
        return HttpResponse(json.dumps(ret))
    return render(request,'html/ajaxTest.html')
