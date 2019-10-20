from accounts.models import Account, Std_Master, Stream, Sem, Div
from django.core.files.storage import FileSystemStorage
from django.conf.urls.static import static


def authenticat(email):
    use = Account.objects.get(email=email)
    if use.is_admin == False:
        return True
    else:
        return False

def up(request,id):
    user = Account.objects.get(id=id)
    std_m = Std_Master.objects.get(user_id=id)
    roll = request.POST['roll']
    enroll = request.POST['enroll']
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    email = request.POST['email']
    stream = request.POST['stream']
    sem = request.POST['sem']
    div = request.POST['div']
    if 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)
        user.img = filename
    else:
        pass
    
    if roll == "":
        pass
    else:
        user.roll = roll

    if enroll == "":
        pass
    else:
        user.enroll = enroll

    if first_name == "":
        pass
    else:
        user.first_name = first_name

    if last_name == "":
        pass
    else:
        user.last_name = last_name

    if email == "nikunj":
        pass
    else:
        user.email = email

    if stream == "Select Sream":
        pass
    else:
        streams = Stream.objects.get(stream_name=stream)
        std_m.stream = streams

    if sem == "Select Semester":
        pass
    else:
        sems = Sem.objects.get(sem_name=sem)
        std_m.sem = sems

    if div == "Select Divition":
        pass
    else:
        divs = Div.objects.get(div_name=div)
        std_m.div = divs
    user.save()
    std_m.save()