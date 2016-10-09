# coding=utf-8
"""wireless URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from managesys import views

urlpatterns = [
    url(r'^$', views.index),  # 默认界面
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register),
    url(r'^login/', views.login),
    url(r'^createAccount/', views.createAccount),
    url(r'^userinfo/', views.userinfo),
    #  url(r'^refreshUserInfo/', views.refreshUserInfo),
    url(r'^userinfo_change/', views.userinfo_change),
    url(r'^stop_service/', views.stop_service),
    url(r'^restore_service/', views.restore_service),
    url(r'^chargeFee/', views.chargeFee),
    url(r'^check_user_usage/', views.checkUserUsage),
    url(r'^check_usage/', views.checkUsage),
    url(r'^new_usage/', views.newUsage)
]
