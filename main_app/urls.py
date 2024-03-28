from django.urls import path, include, re_path
from main_app import views

app_name = 'main_app'

urlpatterns = [

    #registration, login and student tab links

    re_path(r'^registerStudent/', views.registerStudent, name='registerStudent'),
    re_path(r'^registerLab/', views.registerLab, name='registerLab'),
    re_path(r'^registerOther/', views.registerOther, name='registerOther'),
    re_path(r'^registerBTP/', views.registerBTP, name='registerBTP'),
    re_path(r'^registerHOD/', views.registerHOD, name='registerHOD'),
    re_path(r'^user_login/$', views.user_login, name='user_login'),
    re_path(r'^studentLab/', views.studentLab, name='studentLab'),
    re_path(r'^studentBTP/', views.studentBTP, name='studentBTP'),
    re_path(r'^studentOther/', views.studentOther, name='studentOther'),
    re_path(r'^StudentApply/', views.apply_page, name='StudentApply'),
    # re_path(r'^applied/', views.create_applied, name='applied'),
    re_path(r'^change_password/',views.change_password,name='change_password'),
    path('callback', views.callback, name='callback'),

]
