# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login,logout
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import *
import json
from .validation import *
from django.db import transaction

# Create your views here.
# ----------------------------------------------------------------------------------------------------------------
def edit_user_details(request):
    admin=is_kanohi_admin(request)
    if admin:
        params=json.loads(request.body)
        edit_user_details_function(params)
        
    return JsonResponse({"validation": " permission restricted", "status": False})
# ----------------------------------------------------------------------------------------------------------------------------
def create_user(request):
    admin=is_kanohi_admin(request)
    if admin:
        params = json.loads(request.body)
        create_user_function(params)
    else:
        return JsonResponse({"validation": " permission restricted", "status": False})
# ------------------------------------------------------------------------------------------------------------------------
# note: add kanohi admin=recieved hard coded role_type =5 from front end
# --------------------------------------------------------------------------------------------------------------------------------
def add_kanohi_admin(request):
    params = json.loads(request.body)
    admin=is_kanohi_admin(request)
    if admin:
        try:
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
    
    return change_password_function(params)

# ------------------------------------------------------------------------------------------------------------------------
def login_user(request):
    jsonObj = json.loads(request.body)
    username = jsonObj.get('username')
    password = jsonObj.get('password')
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
    params=json.loads(request.body)
    admin=is_kanohi_admin(request)
    franchisee_amin=is_franchisee_admin(request)
    if admin or franchisee_amin:    
        data , massage , status =validate_franchisee(params)
        if status:
            try:
                create_franchisee = Franchisee.objects.create(**data)
                return JsonResponse({"validation": massage, "status": status})
            except Exception as e:
                print(e)    
                return JsonResponse({"validation": 'inconsistence data'})
        else:
            return JsonResponse({"validation": massage, "status": status})
    else:
        return JsonResponse({"validation": " permission restricted", "status": False})

# ---------------------------------------------------------------------------------------------------------------------
def edit_franchisee(request):
    params=json.loads(request.body)
    recived_data=get_recieved_params(params)
    modified_data=get_modified_params(recived_data)
    admin=is_kanohi_admin(request)
    franchisee_amin=is_franchisee_admin(request)
    print(admin)
    if admin or franchisee_amin :   
    
        franchisee_obj=Franchisee.objects.get(id=recived_data["franchisee_id"])
        
        try:
            franchisee_detail=franchisee_obj.get_json()
            franchisee_detail.update(**modified_data)
            franchisee_save=Franchisee.objects.filter(id=recived_data["franchisee_id"]).update(**franchisee_detail)
            
        except Exception as e:
            print(e)
            return JsonResponse({"validation": " error while updating", "status": False})
        return JsonResponse({"validation": "done", "status": True})
    return JsonResponse({"validation": " permission restricted", "status": False})
# ------------------------------------------------------------------------------------------------------------------






