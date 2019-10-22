from django.core import serializers
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import login
import json
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from .models import *
from .forms import authenticat, up
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.
def std_update(request):
    user = Account.objects.get(id=request.session['id']) 
    if request.method == 'POST':
        password = request.POST['password']
        if auth.authenticate(username=user.email,password=password):
            up(request,request.session['id'])
            return std_profile(request)
        else:
            return std_profile(request)
    else:
        return std_profile(request)

def std_profile(request):
    streams = Stream.objects.all()
    std = Account.objects.get(id=request.session['id'])
    std_m = Std_Master.objects.get(user_id=request.session['id'])
    return render(request, "std_profile.html", {'streams' : streams, 'std' : std, 'std_m' : std_m})

def faculty(request):
    feed = Feedback.objects.filter(user_id=request.session['id'])
    lac = list()
    lab = list()
    pro = list()
    for f in feed:
        po = Post.objects.get(id=f.post_id)
        if po.post_name == 'LAC':
            lac.append(f.msg)
        elif po.post_name == 'LAB':
            lab.append(f.msg)
        else:
            pro.append(f.msg)
    # star = {'1':0, '2':0, '3':0, '4':0, '5':0}
    lst1 = []
    lst2 = []
    for f in feed:
        lst1.append(f.q1)
        lst1.append(f.q2)
        lst1.append(f.q3)
        lst1.append(f.q4)
        lst1.append(f.q5)
        lst1.append(f.q6)
        lst1.append(f.q7)
        lst1.append(f.q8)
        lst1.append(f.q9)
        lst1.append(f.q10)
    for i in range(1,6):
        lst2.append(lst1.count(i))
    return render(request, 'faculty.html', {'lst2' : lst2, 'feed' : feed, 'lac' : lac, 'lab' : lab, 'pro' : pro})

def fac_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if authenticat(email) == True:
            if user is not None:
                auth.login(request, user)
                request.session['username'] = user.username
                request.session['email'] = user.email
                request.session['id'] = user.pk
                return redirect('faculty')
            else:
                messages.info(request, 'Invalid Username And Password')
                return redirect('login')
        else:
            messages.info(request, 'You Are Not Login')
            return redirect('login')
    else:
        return render(request, 'fac_login.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if authenticat(email) == True:
            if user is not None:
                auth.login(request, user)
                request.session['username'] = user.username
                request.session['email'] = user.email
                request.session['id'] = user.pk
                return redirect('/')
            else:
                messages.info(request, 'Invalid Username And Password')
                return redirect('login')
        else:
            messages.info(request, 'You Are Not Login')
            return redirect('login')
    else:
        return render(request, 'login.html')

def sign_up(request):
    streams = Stream.objects.all()
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
                return redirect('sign_up')
            else:
                if Account.objects.filter(enroll=enroll).exists():
                    messages.info(request, "Enroll Is Taken...!")
                    return redirect('sign_up')
                else:
                    if Account.objects.filter(roll=roll).exists():
                        messages.info(request, "Roll No Is Taken...!")
                        return redirect('sign_up')
                    else:
                        # print(roll,enroll,first_name,last_name,email)
                        user = Account.objects.create_student(email=email, username=first_name, password=password1, roll=roll, enroll=enroll, first_name=first_name, last_name=last_name)
                        user.save()
                        user = Account.objects.get(email=user.email)
                        streams = Stream.objects.get(stream_name=stream)
                        sems = Sem.objects.get(sem_name=sem)
                        divs = Div.objects.get(div_name=div)
                        std_m = Std_Master.objects.create(user=user, stream=streams, sem=sems, div=divs)
                        std_m.save()
                        return redirect('login') 
        else:
            messages.info(request, "Password Is Not Match...!")
            return redirect('sign_up')
    else:
        return render(request, 'sign_up.html', {'stream' : streams})

def sem_ajax(request):
    stream = request.GET['stream']
    obj_j = serializers.serialize('json', Sem.objects.filter(stream_name=stream))
    obj_list = json.loads( obj_j )
    json_data = json.dumps( obj_list )
    return  HttpResponse(json_data)

def div_ajax(request):
    sem = request.GET['sem']
    obj_j = serializers.serialize('json', Div.objects.filter(sem_name=sem))
    obj_list = json.loads( obj_j )
    json_data = json.dumps( obj_list )
    return  HttpResponse(json_data)

def logoutstd(request):
    auth.logout(request)
    request.session.flush()
    return redirect('/')

def change_password(request):
    if request.method == 'POST':
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        new_pass2 = request.POST['new_pass2']
        if new_pass == new_pass2:
            user = Account.objects.get(id=request.session['id'])
            if auth.authenticate(username=user.email,password=old_pass):
                user.set_password(new_pass)
                user.save()
            else:
                pass
        else:
            pass

    return render(request, 'change_password.html')