"""kanohi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from kanohi_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^kanohi/add/user/', create_user),
    url(r'^kanohi/add/kanohi/admin/', add_kanohi_admin),
    url(r'^kanohi/edit/user/', edit_user_details),
    url(r'^kanohi/change/password/', change_password),
    url(r'^kanohi/create/franchisee/', create_franchisee),
    url(r'^kanohi/edit/franchisee/', edit_franchisee),
    url(r'^kanohi/login/user/', login_user),
    url(r'^kanohi/logout/user/', logout_view),
    url(r'^kanohi/get/all/kanohi/admin/', get_all_kanohi_admin),
    url(r'^kanohi/get/all/kanohi/user/', get_all_users),
    url(r'^kanohi/get/all/kanohi/franchisee/', get_all_franchisee),
]
