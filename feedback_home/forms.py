from accounts.models import *

def get_set(request):
    std = Std_Master.objects.get(user = request.session['id'])
    user = Fac_Master.objects.filter(stream=std.stream, sem=std.sem, div=std.div)
    que = Questions.objects.all()
    dic = dict()
    key = []
    for u in user:
        lst = list()
        ms = str(u.pk)+'_msg'
        obj = request.POST[ms]
        fac = Account.objects.get(id=u.user_id)
        po = Post.objects.get(id=u.post_id)
        lst.append(fac.pk)
        lst.append(po)
        lst.append(obj)
        for q in que:
            st = str(u.pk)+'_'+str(q.que_id)
            obj = request.POST[st]
            lst.append(obj)
            ff = Fac_Master.objects.get(id=u.pk)
        dic[ff]=lst
    std = Account.objects.get(id = request.session['id'])
    for d in dic:
        feed = Feedback.objects.create(std_id=std,fac_id=d,user_id=dic[d][0],post=dic[d][1],
        msg=dic[d][2],
        q1=dic[d][3],
        q2=dic[d][4],
        q3=dic[d][5],
        q4=dic[d][6],
        q5=dic[d][7],
        q6=dic[d][8],
        q7=dic[d][9],
        q8=dic[d][10],
        q9=dic[d][11],
        q10=dic[d][12],
        q11=0,
        q12=0,
        q13=0,
        )
        feed.save()