from django.shortcuts import render, redirect
from accounts.models import *
from feedback_home.forms import get_set

# Create your views here.

def index(request):
    return render(request, 'index.html')

def feedback(request):
    if Feedback.objects.filter(std_id=request.session['id']).exists():
        return redirect('exists')
    else:    
        user = Account.objects.filter(is_staff=True, is_admin=False)
        std = Std_Master.objects.get(user=request.session['id'])
        fac = Fac_Master.objects.filter(stream=std.stream, sem=std.sem, div=std.div)
        que = Questions.objects.all()
        if request.method == 'POST':
            get_set(request)
            return redirect('thank')
        else:
            return render(request, 'feedback.html', {'fac' : fac, 'que' : que, 'user' : user})

def exists(request):
    return render(request, 'exists.html')

def thank(request):
    return render(request, 'thank.html')