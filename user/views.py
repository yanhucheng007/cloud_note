from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.views.decorators.cache import cache_page
from django.urls import reverse
import hashlib
from user.models import User

# Create your views here.
def reg_view(request):
    method = request.method
    if method == 'GET':
        return render(request,'user/register.html')
    elif method == 'POST':
        content = request.POST
        username = content.get('username')
        password = content.get('password')
        repassword = content.get('repassword')
        if password != repassword:
            return render(request,'user/register.html',{'mes':'前后密码输入不一致！'})
        else:
            try:
                User.objects.get(username=username)
            except:
                m = hashlib.md5()
                m.update(password.encode())
                password = m.hexdigest()
                user = User.objects.create(username=username,password=password)
                request.session['username'] = username
                request.session['uid'] = user.id
                request.session.set_expiry(86400)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'user/register.html', {'mes1': '用户已注册！请输入其他用户名！'})

    else:
        pass
@cache_page(timeout=30)
def login_view(request):
    method = request.method
    if method == 'GET':
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect(reverse('index'))
        if request.COOKIES.get('username') and request.COOKIES.get('uid'):
            try:
                user1 = User.objects.get(id=request.COOKIES.get('uid'))
                user2 = User.objects.get(username=request.COOKIES.get('username'))
                if user1 != user2:
                    raise Exception

            except:
               return HttpResponseRedirect(reverse('login_out'))
            else:
                request.session['username'] = request.COOKIES.get('username')
                request.session['uid'] = request.COOKIES.get('uid')
                return HttpResponseRedirect(reverse('index'))
        return render(request, 'user/login.html')
    elif method == 'POST':

        content = request.POST
        username = content.get('username')
        password = content.get('password')
        remember = content.get('remember')
        m = hashlib.md5()
        m.update(password.encode())
        password = m.hexdigest()
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('此用户未注册！')
        else:
            password_r = user.password
            if password == password_r:
                request.session['username'] = username
                request.session['uid'] = user.id
                request.session.set_expiry(86400)
                res = HttpResponseRedirect(reverse('index'))
                if remember:
                    res.set_cookie('uid',user.id,max_age=259200)
                    res.set_cookie('username', username, max_age=259200)
                return res
            else:
                return HttpResponse('密码错误！')
def login_out(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    res = HttpResponseRedirect(reverse('index'))
    if 'username' in request.COOKIES:
        res.delete_cookie('username')
    if 'uid' in request.COOKIES:
        res.delete_cookie('uid')
    return res

