from django.urls import path,include
from accounts import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('', include('feedback_home.urls')),
    path('sem_ajax', views.sem_ajax, name='sem_ajex'),
    path('div_ajax', views.div_ajax, name='div_ajax'),
    path('login', views.login, name='login'),
    path('faculty', views.faculty, name='faculty'),
    path('fac_login', views.fac_login, name='fac_login'),
    path('logoutstd', views.logoutstd, name='logoutstd'),
    path('std_profile', views.std_profile, name='std_profile'),
    path('std_update', views.std_update, name='std_update'),
    path('change_password', views.change_password, name='change_password'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.login, name='password_reset_complete'),
    
]