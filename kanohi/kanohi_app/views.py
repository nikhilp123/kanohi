# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login,logout
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import *
import json
from django.db import transaction
from .helper_functions import is_kanohi_admin,create_user_function,edit_user_details_function,change_password_function,create_franchisee_function,edit_franchisee_function,search_kanohi_admin_function

# Create your views here.
# ----------------------------------------------------------------------------------------------------------------
def edit_user_details(request):
    admin=is_kanohi_admin(request)
    if admin:
        params=json.loads(request.body)
        return edit_user_details_function(params)
        
    return JsonResponse({"validation": " permission restricted", "status": False})
# ----------------------------------------------------------------------------------------------------------------------------
def create_user(request):
    admin=is_kanohi_admin(request)
    print(admin)
    if admin:
        params = json.loads(request.body)
        return create_user_function(params)
    
    return JsonResponse({"validation": " permission restricted", "status": False})
# ------------------------------------------------------------------------------------------------------------------------
# note: add kanohi admin=recieved hard coded role_type =5 from front end
# --------------------------------------------------------------------------------------------------------------------------------
def add_kanohi_admin(request):
    params = json.loads(request.body)
    admin=is_kanohi_admin(request)
    if admin:
        try:
            with transaction.atomic():
                return create_user(request)
        except Exception as e:
            print(e)
            return JsonResponse({"validation": 'inconsistence data'})
    return JsonResponse({"validation": " permission restricted", "status": False})
# ------------------------------------------------------------------------------------------------------------------------------------
def change_password(request):
    if not request.user.is_authenticated():
        return JsonResponse({"redirectConstant": 'LOGIN', "validation":"pleased log in" })

    params=json.loads(request.body)
    user=request.user
    
    return change_password_function(params,user)

# ------------------------------------------------------------------------------------------------------------------------
def login_user(request):
    params = json.loads(request.body)
    username = params.get('username')
    password = params.get('password')
    user = authenticate(request, username=username, password=password)

    if not user:
        return JsonResponse({"validation":'Invalid Login Credentials'})

    if not user.is_active:
        return JsonResponse({"validation":'user is not active', "status": False})

    login(request, user)
    system_user = UserDetails.objects.filter(user=user).first()

    if not system_user:
        return JsonResponse({"validation":'not system user', "status": False})

    try:
        if system_user and int(system_user.role) == UserDetails.DOCTOR:
            return JsonResponse({"redirectUrl":'/systemUserDoctor',"redirectConst":'systemUserDoctor', "status": True})
        elif system_user and int(system_user.role) == UserDetails.LAB_ASSISTANCE:
            return JsonResponse({"redirectUrl":'/systemUserLabAssistance', "status": True})
        elif system_user and int(system_user.role) == UserDetails.FRONT_DESK:
            return JsonResponse({"redirectUrl":'/systemUserFrontDesk', "status": True})
        elif system_user and int(system_user.role) == UserDetails.FRANCHISEE_ADMIN:
            return JsonResponse({"redirectUrl":'/systemUserFranchiseeAdmin', "status": True})
        elif system_user and int(system_user.role)==UserDetails.KANOHI_ADMIN:
            return JsonResponse({"redirectUrl":'/kanohiAdmin', "status": True})
        else:
            return JsonResponse({"validation":'Invalid User', "status": False})
    except Exception as e:
        print (e)        

    return JsonResponse({"validation":'Invalid User', "status": False})
#----------------------------------------------------------------------------------------------------------
def logout_view(request):
    logout(request)
    return JsonResponse({"validation":'logged out', "status": True})
# ------------------------------------------------------------------------------------------------------
def get_all_kanohi_admin(request):
    try:
        persons = UserDetails.objects.filter(role=5)
        list_out=[]
        for person in persons:
            list_out.append(person.get_json())
        return JsonResponse({"data": list_out, "status": True})
    except Exception as e:
            print('Error in get_all_kanohi_admin: ', e)
            return JsonResponse({"validation": "Failed to get all kanohi admin", "status": False})        
# ------------------------------------------------------------------------------------------------------------------
def get_all_users(request):
    try:
        users=UserDetails.objects.exclude(role=UserDetails.KANOHI_ADMIN)
        user_list=[]   
        for user in users:
            user_list.append(user.get_json())
        return JsonResponse({"data": user_list, "status": True})
    except Exception as e:
            print('Error in get_all_users: ', e)
            return JsonResponse({"validation": "Failed to get all users", "status": False})        

# ------------------------------------------------------------------------------------------------------------------
def get_all_franchisee(request):
    try:
        franchisees=Franchisee.objects.all()
        franchisee_list=[]
        for franchisee in franchisees:
            franchisee_list.append(franchisee.get_json())
        return JsonResponse({"data": franchisee_list, "status": True})
    except Exception as e:
            print('Error in get_all_franchisee: ', e)
            return JsonResponse({"validation": "Failed to get all franchisee", "status": False})        

# ----------------------------------------------------------------------------------------------------------------------------
def create_franchisee(request):
    admin=is_kanohi_admin(request)
    if admin:    
        params=json.loads(request.body)
        return create_franchisee_function(params)
    else:
        return JsonResponse({"validation": " permission restricted", "status": False})

# ---------------------------------------------------------------------------------------------------------------------
def edit_franchisee(request):
    admin=is_kanohi_admin(request)
    if admin:   
        params=json.loads(request.body)
        return edit_franchisee_function(params)
    return JsonResponse({"validation": " permission restricted", "status": False})
# ------------------------------------------------------------------------------------------------------------------
# results = BlogPost.objects.filter(Q(title__icontains=your_search_query) | Q(intro__icontains=your_search_query) | Q(content__icontains=your_search_query))
def search_kanohi_admin(request):
    admin=is_kanohi_admin(request)
    if admin:   
        params=json.loads(request.body)
        return search_kanohi_admin_function(params)
    return JsonResponse({"validation": " permission restricted", "status": False})
#------------------------------------------------------------------------------------------------------------------------- 




