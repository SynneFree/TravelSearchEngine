from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import *
from myapp.forms import *
# from django.db.models import Q my


# Create your views here.

def index(request):
    return render(request,'html/home.html')

def search(request):
    search_field=request.GET.get('search_field',None)
    msg='无效搜索'
    context={
        'msg':msg
    }
    if search_field:
        context={
            searchindex(search_field)
        }
    return render(request,'html/result.html',context)




def login(request):
    if request.session.get('is_login',None):
        return redirect('../')
 
    if request.method == "POST":
        login_form = UserForm(request.POST)
        print(login_form.is_valid()) # 这一行必须要有，不然下面cleaned_data会出错
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        
        user = User.objects.get(pk=username)
        if (user):
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_name'] = user.username
                print("login success")                
                return redirect('../')
            else:
                message = "密码不正确！"
        else:
            message = "用户不存在！"

        return render(request, 'html/login.html', locals())
    login_form = UserForm()
    return render(request, 'html/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        return redirect("../")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        print(register_form.is_valid())  # 获取数据
        username = register_form.cleaned_data['username']
        password1 = register_form.cleaned_data['password1']
        password2 = register_form.cleaned_data['password2']
        email = register_form.cleaned_data['email']  
        if password1 != password2:  # 判断两次密码是否相同
            message = "两次输入的密码不同！"
            return render(request, 'html/register.html', locals())
        else:
            same_name_user = User.objects.filter(pk=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
                return render(request, 'html/register.html', locals())
            same_email_user = User.objects.filter(email=email)
            if same_email_user:  # 邮箱地址唯一
                message = '该邮箱地址已被注册，请使用别的邮箱！'
                return render(request, 'html/register.html', locals())
            # 当一切都OK的情况下，创建新用户

            new_user = User.objects.create(pk=username,email=email,password=password1)
            new_user.save()
            return redirect('../login')  # 自动跳转到登录页面
    else:
        register_form = RegisterForm()
        return render(request, 'html/register.html', locals())
 
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("../")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("../")