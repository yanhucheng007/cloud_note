from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Note
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
import csv

# Create your views here.
def check_login(fn):
    def wrap(request,*args,**kwargs):
        if 'username' in request.session and 'uid' in request.session:
            return fn(request,*args,**kwargs)
        return HttpResponseRedirect(reverse('login'))

    return wrap


@check_login
def list_note(request):
    page_num = request.GET.get('page',1)
    uid = request.session['uid']
    notes = Note.objects.filter(user_id=uid)
    paginator = Paginator(notes,5)
    page = paginator.page(page_num)
    return render(request,'note/list.html',{'notes':page})
@check_login
def update(request):
    if request.method == 'GET':
        note_id = request.GET.get('note_id')
        if note_id:
            try:
                note = Note.objects.get(id=note_id)
            except:
                return HttpResponseRedirect(reverse('login_out'))
            else:

                title = note.title
                content = note.content
                note_file = note.note_file
                return render(request, 'note/update.html', {'title':title, 'content':content, 'id':note.id,'note_file':note_file})
        else:
            return render(request, 'note/update.html')
    elif request.method == 'POST':
        note_id = request.POST.get('note_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        note_file = request.FILES.get('note_file')
        if note_id:
            try:
                note = Note.objects.get(id=note_id)
            except:
                return HttpResponse('没有这条记录')
            else:
                note.title = title
                note.content = content
                note.note_file.delete()
                note.note_file = note_file
                note.save()
                return HttpResponseRedirect(reverse('list_note'))
        else:
            Note.objects.create(title=title,content=content,user_id=request.session['uid'],note_file=note_file)
            return HttpResponseRedirect(reverse('list_note'))
@check_login
def delete_note(request):
    note_id = request.GET.get('note_id')
    if note_id:
        try:
            note = Note.objects.get(id=note_id)
        except:
            return HttpResponseRedirect(reverse('login_out'))
        else:
            note.delete()
            return HttpResponseRedirect(reverse('list_note'))
    else:
        return HttpResponseRedirect(reverse('list_note'))

def detail(request):
    note_id = request.GET.get('note_id')
    try:
        note = Note.objects.get(id=note_id)
    except:
        return HttpResponse('没有这条记录')
    else:
        name = str(note.note_file)
        newname = name.replace('note_file/','')
        return render(request,'note/detail.html',{'note':note,'name':newname})


@check_login
def export_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="my_note.csv"'
    uid = request.session['uid']
    notes = Note.objects.filter(user_id=uid)
    writer = csv.writer(response)
    writer.writerow(['标题','内容','创建时间','最后一次修改时间'])
    for note in notes:
        title = note.title
        content = note.content
        create_time = note.create_time
        update_time = note.update_time
        writer.writerow([title,content,create_time,update_time])
    return response
