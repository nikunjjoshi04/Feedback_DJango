from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyaccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an Username")

        user = self.model(
            email = self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True     
        user.save(using=self._db)
        return user
    
    def create_student(self, email, username, roll, enroll, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an Username")

        user = self.model(
            email = self.normalize_email(email),
            username=username,
            roll=roll,
            enroll=enroll,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    roll = models.IntegerField(blank=True, null=True)
    enroll = models.IntegerField(blank=True, null=True)
    img = models.ImageField(upload_to='pics/', default="None")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyaccountManager()

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, object=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class Stream(models.Model):
    stream_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.stream_name

class Sem(models.Model):
    sem_name = models.CharField(max_length=100)
    stream_name = models.ForeignKey(Stream, on_delete=models.CASCADE)

    def __str__(self):
        return self.sem_name


class Div(models.Model):
    div_name = models.CharField(max_length=100)
    stream_name = models.ForeignKey(Stream, on_delete=models.CASCADE)
    sem_name = models.ForeignKey(Sem, on_delete=models.CASCADE)
    def __str__(self):
        return self.div_name

class Post(models.Model):
    post_name = models.CharField(max_length=100)
    def __str__(self):
        return self.post_name

class Subject(models.Model):
    sub_code = models.IntegerField()
    sub_name = models.CharField(max_length=100)
    stream_name = models.ForeignKey(Stream, on_delete=models.CASCADE)
    sem_name = models.ForeignKey(Sem, on_delete=models.CASCADE)
    def __str__(self):
        return self.sub_name


class Std_Master(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    sem = models.ForeignKey(Sem, on_delete=models.CASCADE)
    div = models.ForeignKey(Div, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

class Fac_Master(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    sem = models.ForeignKey(Sem, on_delete=models.CASCADE)
    div = models.ForeignKey(Div, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

class Questions(models.Model):
    que_id = models.IntegerField()
    que = models.CharField(max_length=225)

class Csv(models.Model):
    csv = models.FileField(upload_to='pics')
    csv_tag = models.CharField(max_length=50)
    csv_flag = models.CharField(max_length=50)
    def __str__(self):
        return str(self.csv_tag)

class Feedback(models.Model):
    std_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    fac_id = models.ForeignKey(Fac_Master, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=50)
    msg = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
    q5 = models.IntegerField()
    q6 = models.IntegerField()
    q7 = models.IntegerField()
    q8 = models.IntegerField()
    q9 = models.IntegerField()
    q10 = models.IntegerField()
    q11 = models.IntegerField()
    q12 = models.IntegerField()
    q13 = models.IntegerField()
