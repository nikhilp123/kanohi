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
def is_kanohi_admin(request):
    authentication=request.user.is_authenticated()
    if authentication: 
        user_cnf=UserDetails.objects.get(user=request.user)
        user_role=user_cnf.role
        print(user_role)
        if int(user_role)==UserDetails.KANOHI_ADMIN:
            return True
        else:    
            return False
    else:
        return False 
#--------------------------------------------------------------------------------------------------------------------------- 
def is_franchisee_admin(request):
    authentication=request.user.is_authenticated()
    if authentication: 
        user_cnf=UserDetails.objects.get(user=request.user)
        user_role=user_cnf.role
        print(user_role)
        if int(user_role)==UserDetails.FRANCHISEE_ADMIN:
            return True
        else:    
            return False
    else:
        return False 

#---------------------------------------------------------------------------------------------------------------------------
def edit_user_details(request):
    params=json.loads(request.body)
    recived_data=get_users_recieved_params(params)
    modified_data=get_users_modified_params(recived_data)
    admin=is_kanohi_admin(request)
    franchisee_amin=is_franchisee_admin(request)
    print(admin)
    if admin or franchisee_amin:   
    
        user_detail_obj=UserDetails.objects.get(id=recived_data["user_id"])
        
        try:
            user_detail=user_detail_obj.get_json()
            user_detail.update(**modified_data)
            user_save=UserDetails.objects.filter(id=recived_data["user_id"]).update(**user_detail)
            
        except Exception as e:
            print(e)
            return JsonResponse({"validation": "error while updating", "status": False})
        return JsonResponse({"validation": "done", "status": True})
    return JsonResponse({"validation": " permission restricted", "status": False})
# ----------------------------------------------------------------------------------------------------------------------------
def create_user(request):
    params = json.loads(request.body)
    admin=is_kanohi_admin(request)
    franchisee_amin=is_franchisee_admin(request)
    if admin or franchisee_amin :
        username = params.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            return JsonResponse({"validation": 'Member already registered in the system', "status": False})

        user_obj = User()
        user_obj.username = username
        user_obj.set_password(str(params.get('password')))
        user_obj.save()
        user_id=user_obj.id
        data , massage , status = validate_user(params,user_id)
        if status:
            try:
                personal_info,create= UserDetails.objects.create(**data)
                print(personal_info, create)
                return JsonResponse({"validation": massage, "status": status})
            except Exception as e:
                print(e)    
                return JsonResponse({"validation": 'inconsistence data'})
        else:
            return JsonResponse({"validation": massage, "status": status})
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
    user=request.user
    new_password = str(jsonObj.get('newPassword'))
    confirm_password = str(jsonObj.get('confirmPassword'))
    length_password = len(new_password)
    if (length_password < 4):
        return JsonResponse({"validation": 'Passwordis to short. Need minimum of 8 characters', "status": False})
    if new_password != confirm_password:
        return JsonResponse({"validation": 'Passwords do not match', "status": False})
    else:
        user.set_password(confirm_password)
        user.save()
        return JsonResponse({"redirectConstant": "DASHBOARD", "status": True})

# ------------------------------------------------------------------------------------------------------------------------
def login_user(request):
    jsonObj = json.loads(request.body)
    print (jsonObj)
    username = jsonObj.get('username')
    password = jsonObj.get('password')
    print(username , password)
    user = authenticate(request, username=username, password=password)
    print(user)

    if not user:
        return JsonResponse({"validation":'Invalid Login Credentials'})

    if not user.is_active:
        return JsonResponse({"validation":'user is not active', "status": False})

    login(request, user)
    system_user = UserDetails.objects.filter(user=user).first()

    if not system_user:
        return JsonResponse({"validation":'not system user', "status": False})

    print(system_user)    
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
    return JsonResponse({"validation":'logged out', "status": False})

# ------------------------------------------------------------------------------------------------------
def get_all_kanohi_admin(request):
    try:
        kwargs = {}
        kwargs["role"] = 5   
        persons = UserDetails.objects.filter(**kwargs)
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






