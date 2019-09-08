"""BM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from bm_project import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.home, name="home"),
    path('rehome/', views.rehome),
    path('searchall_elements/', views.searchall_elements),
    path('searchall_formula/', views.searchall_formula),
    path('searchall_ids/', views.searchall_ids),
    path('signup/', views.signup),
    path('login/', views.login),
    path('door/', views.door),
    path('chart/', views.chart),
    path('search_id/', views.search_id),
    path('search_elements/', views.search_elements),
    path('search_formula/', views.search_formula),
    path('vasp/', views.vasp),
    path('search_id/gotovasp/', views.readytovasp),
    path('search_formula/gotovasp/', views.readytovasp),
    path('search_elements/gotovasp/', views.readytovasp),
    path('automatic/', views.automatic),
    path('manual/', views.manual),
    path('home/', views.home),
    path('taskmanage/', views.taskmanage),
    path('logout/', views.logout),
    path('materialdetail/', views.materialdetail),
    path('her_data/', views.her_data),
    path('high_throughput/', views.high_throughput),
    path('svc/', views.svc),
    path('dtc/', views.dtc),
    path('pca/', views.pca),
    path('high_throughput_go/', views.high_throughput_go),
    path('serverinput/', views.serverinput),
    path('readytohigh_throughput/', views.readytohigh_throughput),
    path('tutorials/', views.tutorials),
    path('taskmanage_completed/',views.taskmanage_completed),






]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
