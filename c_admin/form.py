from accounts.models import Account, Std_Master, Stream, Sem, Div, Post, Subject, Fac_Master, Feedback, Questions
from django.core.files.storage import FileSystemStorage

# Create your forms here.

def csv_que_up(request):
    e_path = 'E:/dev/feedback/'
    l1,l2 = request.POST['csv'].split('/')
    csv_file = e_path+l1
    data = open(csv_file,'r')
    lst1 = []
    iterdata = iter(data)
    next(iterdata)
    for i in iterdata:
        i,j = i.split('\n')
        lst = [i for i in i.split(',')]
        lst1.append(lst)
    for i in lst1:
        que = Questions.objects.create(que_id=i[0],que=i[1])
        que.save()
    return True

def csv_sub_up(request):
    e_path = 'E:/dev/feedback/'
    l1,l2 = request.POST['csv'].split('/')
    csv_file = e_path+l1
    data = open(csv_file,'r')
    lst1 = []
    iterdata = iter(data)
    next(iterdata)
    for i in iterdata:
        i,j = i.split('\n')
        lst = [i for i in i.split(',')]
        lst1.append(lst)
    for i in lst1:
        stream = Stream.objects.get(stream_name=i[2])
        sem = Sem.objects.get(sem_name=i[3])
        sub = Subject.objects.create(sub_code=i[0],sub_name=i[1],stream_name=stream,sem_name=sem)
        sub.save()
    return True

def csv_post_up(request):
    e_path = 'E:/dev/feedback/'
    l1,l2 = request.POST['csv'].split('/')
    csv_file = e_path+l1
    data = open(csv_file,'r')
    iterdata = iter(data)
    next(iterdata)
    for i in iterdata:
        i,j = i.split('\n')
        post = Post.objects.create(post_name=i)
        post.save()
    return True

def csv_div_up(request):
    e_path = 'E:/dev/feedback/'
    l1,l2 = request.POST['csv'].split('/')
    csv_file = e_path+l1
    data = open(csv_file,'r')
    lst1 = []
    iterdata = iter(data)
    next(iterdata)
    for i in iterdata:
        i,j = i.split('\n')
        lst = [i for i in i.split(',')]
        lst1.append(lst)
    for i in lst1:
        stream = Stream.objects.get(stream_name=i[1])
        sem = Sem.objects.get(sem_name=i[2])
        div = Div.objects.create(div_name=i[0],stream_name=stream,sem_name=sem)
        div.save()
    return True

def csv_sem_up(request):
    e_path = 'E:/dev/feedback/'
    l1,l2 = request.POST['csv'].split('/')
    csv_file = e_path+l1
    data = open(csv_file,'r')
    lst1 = []
    iterdata = iter(data)
    next(iterdata)
    for i in iterdata:
        i,j = i.split('\n')
        lst = [i for i in i.split(',')]
        lst1.append(lst)
    for i in lst1:
        stream = Stream.objects.get(stream_name=i[1])
        sem = Sem.objects.create(sem_name=i[0],stream_name=stream)
        sem.save()
    return True

def csv_stream_up(request):
    e_path = 'E:/dev/feedback/'
    l1,l2 = request.POST['csv'].split('/')
    csv_file = e_path+l1
    data = open(csv_file,'r')
    iterdata = iter(data)
    next(iterdata)
    for i in iterdata:
        i,j = i.split('\n')
        stream = Stream.objects.create(stream_name=i)
        stream.save()
    return True

def csv_fac_up(request):
    e_path = 'E:/dev/feedback/'
    l1,l2 = request.POST['csv'].split('/')
    csv_file = e_path+l1
    data = open(csv_file,'r')
    lst1 = []
    iterdata = iter(data)
    next(iterdata)
    for i in iterdata:
        i,j = i.split('\n')
        lst = [i for i in i.split(',')]
        lst1.append(lst)        
    for i in lst1:
        user = Account.objects.create(
            username=i[0], 
            is_staff=True, 
            first_name=i[0], 
            last_name=i[1], 
            mobile=i[3], 
            email=i[2]
            )
        user.set_password(123)    
        user.save()
    return True

def csv_std_up(request):
    e_path = 'E:/dev/feedback/'
    l1,l2 = request.POST['csv'].split('/')
    csv_file = e_path+l1
    data = open(csv_file,'r')
    lst1 = []
    iterdata = iter(data)
    next(iterdata)
    for i in iterdata:
        i,j = i.split('\n')
        lst = [i for i in i.split(',')]
        lst1.append(lst)        
    for i in lst1:
        user = Account.objects.create_student(
            email=i[4], 
            username=i[2], 
            password=i[8], 
            roll=i[0], 
            enroll=i[1], 
            first_name=i[2],
            last_name=i[3]
            )
        user.save()
        user = Account.objects.get(email=user.email)
        streams = Stream.objects.get(stream_name=i[5])
        sems = Sem.objects.get(sem_name=i[6])
        divs = Div.objects.get(div_name=i[7])
        std_m = Std_Master.objects.create(user=user, stream=streams, sem=sems, div=divs)
        std_m.save()
    return True    

def fac_aj(fac_obj):
    lst=[]
    for f in fac_obj:
        dic = {"model": "accounts.fac_master", "pk": "0", "fields": {"user": "0", "stream": "0", "sem": "0", "div": "0", "post": "0", "subject": "0"}}
    
        dic['pk'] = str(f.pk)
        dic['fields']['user'] = str(f.user)
        dic['fields']['stream'] = str(f.stream)
        dic['fields']['sem'] = str(f.sem)
        dic['fields']['div'] = str(f.div)
        dic['fields']['post'] = str(f.post)
        dic['fields']['subject'] = str(f.subject)
        lst.append(dic)
    return lst

def fac_m_allo(request):
    user = request.POST['user']
    stream = request.POST['stream']
    sem = request.POST['sem']
    div = request.POST['div']
    post = request.POST['post']
    sub = request.POST['sub']
    user = Account.objects.get(id=user)
    stream = Stream.objects.get(id=stream)
    sem = Sem.objects.get(id=sem)
    div = Div.objects.get(id=div)
    post = Post.objects.get(id=post)
    sub = Subject.objects.get(id=sub)
    if Fac_Master.objects.filter(user = user, stream=stream,sem=sem,div=div,post=post,subject=sub).exists():
        return False
    else:
        fac_m = Fac_Master.objects.create(user = user, stream=stream,sem=sem,div=div,post=post,subject=sub)
        fac_m.save()
        return True

def pro_fac_m_allo(request,id):
    stream = request.POST['stream']
    sem = request.POST['sem']
    div = request.POST['div']
    post = request.POST['post']
    sub = request.POST['sub']
    user = Account.objects.get(id=id)
    stream = Stream.objects.get(id=stream)
    sem = Sem.objects.get(id=sem)
    div = Div.objects.get(id=div)
    post = Post.objects.get(id=post)
    sub = Subject.objects.get(id=sub)
    if Fac_Master.objects.filter(user = user, stream=stream,sem=sem,div=div,post=post,subject=sub).exists():
        return False
    else:
        fac_m = Fac_Master.objects.create(user = user, stream=stream,sem=sem,div=div,post=post,subject=sub)
        fac_m.save()
        return True


def authenticat(email):
    use = Account.objects.get(email=email)
    if use.is_admin == True:
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
        
def up_fac(request,id):
    user = Account.objects.get(id=id)
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    email = request.POST['email']
    mobile = request.POST['mobile']

    if 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)
        user.img = filename
    else:
        pass

    if first_name == "":
        pass
    else:
        user.first_name = first_name

    if last_name == "":
        pass
    else:
        user.last_name = last_name

    if email == "":
        pass
    else:
        user.email = email

    if mobile == "":
        pass
    else:
        user.mobile = mobile
    user.save()

def make(fee):
    feed = Feedback.objects.all()
    dic = dict()
    for f in feed:
        lst = list()
        std = Account.objects.get(first_name=f.std_id)  
        lst.append(std.first_name)
        fac = Fac_Master.objects.get(user=f.fac_id)
        lst.append(fac.first_name)
        lst.append(f.msg)
        lst.append(f.q1)
        lst.append(f.q2)
        dic[f.pk] = lst
    return dic    