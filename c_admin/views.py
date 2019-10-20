from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from accounts.models import *
import json
import csv
from django.conf import settings
from django.http import HttpResponse,HttpRequest
from django.core import serializers
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .form import *

# Create your views here.

def csv_up(request):
    csv = Csv.objects.all()
    if request.method == 'POST':
        l1,l2 = request.POST['csv'].split('/')
        if l2 == 'stream':
            csv_stream_up(request)
        elif l2 == 'sem':
            csv_sem_up(request)
        elif l2 == 'post':
            csv_post_up(request)
        elif l2 == 'sub':
            csv_sub_up(request)
        elif l2 == 'que':
            csv_que_up(request)
        elif l2 == 'div':
            csv_div_up(request)
        elif l2 == 'std':
            csv_std_up(request)
        elif l2 == 'fac':
            csv_fac_up(request)
        else:
            pass
    else:
        pass
    return render(request, 'csv_up.html', {'csv' : csv})

def admin_feedback(request):
    feed = Feedback.objects.all()
    return render(request, 'admin_feedback.html', {'feed' : feed})

def add_csv(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        csv_tag = request.POST['tag']
        csv_flag = request.POST['flag']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name,csv_file)
        uploaded_file_url = fs.url(filename)
        csv = Csv.objects.create(csv=filename,csv_tag=csv_tag,csv_flag=csv_flag)
        csv.save()
        return render(request, "add_csv.html")
    else:
        return render(request, "add_csv.html")

def delete_fac_allo(request,id5):
    fac_m = Fac_Master.objects.get(id = id5)
    fac_m.delete()    
    return redirect('fac_allo')

def fac_allo(request):
    fac = Account.objects.filter(is_staff=True, is_superuser=False)
    stream = Stream.objects.all()
    post = Post.objects.all()
    fac_m = Fac_Master.objects.all() 
    if request.method == 'POST':
        if fac_m_allo(request) is False:
            messages.info(request, "Email Is Taken...!")
            return render(request, 'fac_allo.html', {'stream' : stream, 'post' : post, 'fac_m' : fac_m, 'fac' : fac})            
        else:
            return redirect('fac_allo')
    else:
        return render(request, 'fac_allo.html', {'stream' : stream, 'post' : post, 'fac_m' : fac_m, 'fac' : fac})

def pro_fac_allo(request):
    stream = Stream.objects.all()
    post = Post.objects.all()
    fac_m = Fac_Master.objects.all() 
    if request.method == 'POST':
        if pro_fac_m_allo(request,request.session['update_id']) is False:
            messages.info(request, "Email Is Taken...!")
            return fac_pro(request,request.session['update_id'])
        else:
            return fac_pro(request,request.session['update_id'])
    else:
        return fac_pro(request,request.session['update_id'])

def update_fac(request):
    user = Account.objects.get(id=request.session['update_id']) 
    if request.method == 'POST':
        up_fac(request,request.session['update_id'])
        return fac_pro(request,request.session['update_id'])
    else:
        return fac_pro(request,request.session['update_id'])

def que_update(request): 
    if request.method == 'POST':
        que_id = request.POST['que_id']
        que = request.POST['que']
        ques = Questions.objects.get(que_id=que_id)
        ques.que = que
        ques.save()
        return redirect('add_que')
    else:
        return redirect('add_que')

def update_std(request):
    user = Account.objects.get(id=request.session['update_id']) 
    if request.method == 'POST':
        up(request,request.session['update_id'])
    else:
        return std_pro(request,request.session['update_id'])
    return std_pro(request,request.session['update_id'])

def students(request):
    std = Account.objects.filter(is_staff=False)
    return render(request, "students.html",{'std' : std})

def delete_fac(request, id):
    fac = Account.objects.get(id = id)
    fac.delete()
    return redirect('adminc')

def delete_std(request, idd):
    std = Account.objects.get(id = idd)
    std.delete()
    return redirect('students')

def delete_que(request, id6):
    que = Questions.objects.get(id = id6)
    que.delete()
    return redirect('add_que')

def add_fac(request):
    if request.method == 'POST': 
        first_name = request.POST['fac_fname']
        last_name = request.POST['fac_lname']
        mobile = request.POST['fac_mobile']
        email = request.POST['fac_email']
        user = Account.objects.create(username=first_name, is_staff=True, first_name=first_name, last_name=last_name, mobile=mobile, email=email)
        user.save()
        return redirect('add_fac')
    else:
        return render(request, "add_fac.html")

def add_que(request):
    ques = Questions.objects.all()
    if request.method == 'POST': 
        que_id = request.POST['que_id']
        que = request.POST['que']
        quest = Questions.objects.create(que_id=que_id, que=que)
        quest.save()
        return redirect('add_que')
    else:
        return render(request, "add_que.html", {'ques' : ques})

def add_std(request):
    stream = Stream.objects.all()
    if request.method == 'POST':
        roll = request.POST['roll']
        enroll = request.POST['enroll']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        stream = request.POST['stream']
        sem = request.POST['sem']
        div = request.POST['div']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if Account.objects.filter(email=email).exists():
                messages.info(request, "Email Is Taken...!")
                return redirect('add_std')
            else:
                user = Account.objects.create_student(email=email, username=first_name, password=password1, roll=roll, enroll=enroll, first_name=first_name, last_name=last_name)
                user.save()
                user = Account.objects.get(email=user.email)
                streams = Stream.objects.get(stream_name=stream)
                sems = Sem.objects.get(sem_name=sem)
                divs = Div.objects.get(div_name=div)
                std_m = Std_Master.objects.create(user=user, stream=streams, sem=sems, div=divs)
                std_m.save()
                return redirect('add_std') 
        else:
            messages.info(request, "Password Is Not Match...!")
            return redirect('add_std')
    else:
        return render(request, "add_std.html",{'stream' : stream})

def sem_ajax(request):
    stream = request.GET['stream']
    obj_j = serializers.serialize('json', Sem.objects.filter(stream_name=stream))
    obj_list = json.loads( obj_j )
    json_data = json.dumps( obj_list )    
    return  HttpResponse(json_data)

def fac_ajax_srch(request):
    fac = request.GET['fac']
    fac_obj = Fac_Master.objects.filter(user=fac)
    lst = fac_aj(fac_obj)
    json_data = json.dumps( lst )
    return  HttpResponse(json_data)

def stream_ajax_srch(request):
    stream = request.GET['stream']
    stream_obj = Fac_Master.objects.filter(stream=stream)
    lst = fac_aj(stream_obj)
    json_data = json.dumps( lst )
    return  HttpResponse(json_data)

def post_ajax_srch(request):
    post = request.GET['post']
    post_obj = Fac_Master.objects.filter(post=post)
    lst = fac_aj(post_obj)
    json_data = json.dumps( lst )
    return  HttpResponse(json_data)

def sub_ajax_srch(request):
    subject = request.GET['subject']
    subject_obj = Fac_Master.objects.filter(subject=subject)
    lst = fac_aj(subject_obj)
    json_data = json.dumps( lst )
    return  HttpResponse(json_data)

def sem_ajax_srch(request):
    stream = request.GET['stream']
    sem = request.GET['sem']
    sem_obj = Fac_Master.objects.filter(stream=stream, sem=sem)
    lst = fac_aj(sem_obj)
    json_data = json.dumps( lst )
    return  HttpResponse(json_data)

def div_ajax_srch(request):
    stream = request.GET['stream']
    sem = request.GET['sem']
    div = request.GET['div']
    div_obj = Fac_Master.objects.filter(stream=stream, sem=sem, div=div)
    lst = fac_aj(div_obj)
    json_data = json.dumps( lst )
    return  HttpResponse(json_data)

def sub_ajax(request):
    sem = request.GET['sem']
    obj_j = serializers.serialize('json', Subject.objects.filter(sem_name=sem))
    obj_list = json.loads( obj_j )
    json_data = json.dumps( obj_list )
    return HttpResponse(json_data)

        
def div_ajax(request):
    sem = request.GET['sem']
    obj_j = serializers.serialize('json', Div.objects.filter(sem_name=sem))
    obj_list = json.loads( obj_j )
    json_data = json.dumps( obj_list )    
    return  HttpResponse(json_data)

def fac_pro(request, id3):
    request.session['update_id'] = id3
    stream = Stream.objects.all()
    post = Post.objects.all()
    fac = Account.objects.get(id=id3)
    fac_m = Fac_Master.objects.filter(user=id3)
    return render(request, "fac_pro.html", {'stream' : stream, 'fac' : fac, 'post' : post, 'fac_m' : fac_m})

def std_pro(request, id4):
    request.session['update_id'] = id4
    stream = Stream.objects.all()
    std = Account.objects.get(id=id4)
    std_m = Std_Master.objects.get(user=id4)
    return render(request, "std_pro.html", {'stream' : stream, 'std' : std, 'std_m' : std_m})

def adminc(request):
    if 'admin_username' in request.session:
        fac = Account.objects.filter(is_staff=True, is_superuser=False)
    if 'admin_username' not in request.session :
        return redirect('admin_login')
    return render(request, "admin.html", {'fac' : fac})

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if authenticat(email) == True:
            if user is not None:
                auth.login(request, user)
                request.session['admin_username'] = user.username
                request.session['admin_email'] = user.email
                request.session['admin_id'] = user.pk
                return redirect('adminc')
            else:
                messages.info(request, 'Invalid Username And Password')
                return redirect('admin_login')
        else:
            messages.info(request, 'You Are Not Admin')
            return redirect('admin_login')
    else:
        return render(request, 'admin_login.html')

def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect('admin_login')