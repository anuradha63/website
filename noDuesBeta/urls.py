"""noDuesBeta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from main_app import views

urlpatterns = [

    re_path(r'^$', views.mainPage, name='mainPage'),
    re_path(r'^studentIndex/$', views.studentIndex, name='studentIndex'),
    re_path(r'^labIndex/$', views.labIndex, name='labIndex'),
    re_path(r'^otherIndex/$', views.otherIndex, name='otherIndex'),
    re_path(r'^btpIndex/$', views.btpIndex, name='btpIndex'),
    re_path(r'^hodIndex/$', views.hodIndex, name='hodIndex'),
    re_path(r'^labAccountRequests/$', views.hod_lab_approval_page, name='labAccountRequests'),
    re_path(r'^btpAccountRequests/$', views.hod_btp_approval_page, name='btpAccountRequests'),
    re_path(r'^main_app/',include('main_app.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^logout/$', views.user_logout, name='logout'),
    re_path(r'^student_logout/$', views.student_logout, name='student_logout'),
    path('signino', views.sign_ino, name='signino'),
    re_path(r'^heavenIndex/',views.heavenIndex,name='heavenIndex'),


]
