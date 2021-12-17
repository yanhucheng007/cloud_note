from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index_empty(request):
    return HttpResponseRedirect(reverse('index'))
def index(request):
    if 'username' in request.session and 'uid' in request.session:
        context = {'username':request.session['username']}
    elif 'username' in request.COOKIES and 'uid' in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    else:
        context = {}
    return render(request,'index/index.html',context)

