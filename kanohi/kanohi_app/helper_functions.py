import os, re, datetime, json, uuid
from kanohi.settings import BASE_DIR, DEBUG
from django.contrib.auth import authenticate, login,logout
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.db import transaction
from .models import UserDetails, User,Franchisee
from .validation import validate_user,get_users_recieved_params,get_users_modified_params,validate_franchisee,get_franchisee_modified_params,get_franchisee_recieved_params

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def convert_date_to_epoch(date):
    return int(date.strftime('%s'))*1000 if date else None

def convert_epoch_to_date(epoch):
    return datetime.datetime.fromtimestamp(int(epoch)/1000.0) if epoch else None

def convert_time_to_epoch(time):
    return int(datetime.datetime.now().replace(hour=time.hour, minute=time.minute, second=0, microsecond=0).strftime('%s'))*1000 if time else None

def convert_epoch_to_time(epoch):
    return datetime.datetime.fromtimestamp(int(epoch)/1000.0).time() if epoch else None
# ---------------------------------------------------------------------------------------------------------------------------------------------------------
def is_kanohi_admin(request):
    authentication=request.user.is_authenticated()
    if authentication: 
        user_cnf=UserDetails.objects.get(user=request.user)
        user_role=user_cnf.role
        print(user_role)
        if int(user_role)==UserDetails.KANOHI_ADMIN:
            print("true")
            return True
        else:    
            return False
    else:
        return False 

#---------------------------------------------------------------------------------------------------------------------------
def edit_user_details_function(params):
    recived_data=get_users_recieved_params(params)
    modified_data=get_users_modified_params(recived_data)

    user_detail_obj=UserDetails.objects.get(id=recived_data["user_id"])
    
    try:
        user_detail=user_detail_obj.get_json()
        user_detail.update(**modified_data)
        user_save=UserDetails.objects.filter(id=recived_data["user_id"]).update(**user_detail)
        
    except Exception as e:
        print(e)
        return JsonResponse({"validation": "error while updating", "status": False})
    return JsonResponse({"validation": "done", "status": True})

#--------------------------------------------------------------------------------------------------------- 
def create_user_function(params):
    username = params.get('username')
    user = User.objects.filter(username=username).first()
    if user:
        return JsonResponse({"validation": 'Member already registered in the system', "status": False})

    try:
        with transaction.atomic():
            user_obj = User()
            user_obj.username = username
            user_obj.set_password(str(params.get('password')))
            user_obj.save()
            user_id=user_obj.id
            print("user_id: ",user_id)
            data , massage , status = validate_user(params,user_id)
            print("status: ",status)
            if status:
                    personal_info= UserDetails.objects.create(**data)
                    print(personal_info)
                    return JsonResponse({"validation": massage, "status": status})
            else:
                return JsonResponse({"validation": massage, "status": status})
    except Exception as e:
        print(e)
        return JsonResponse({"validation": 'inconsistence data'})
    return JsonResponse({"validation": massage, "status": status})
               
#----------------------------------------------------------------------------------------------------------------------- 
def change_password_function(params,user):
    user=user
    new_password = str(params.get('newPassword'))
    confirm_password = str(params.get('confirmPassword'))
    length_password = len(new_password)
    if (length_password < 4):
        return JsonResponse({"validation": 'Passwordis to short. Need minimum of 8 characters', "status": False})
    if new_password != confirm_password:
        return JsonResponse({"validation": 'Passwords do not match', "status": False})
    else:
        user.set_password(confirm_password)
        user.save()
        return JsonResponse({"redirectConstant": "abc", "status": True})

#---------------------------------------------------------------------------------------------------------------------
# def login_user_function(params):
     
# --------------------------------------------------------------------------------------------
def create_franchisee_function(params):
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
#-------------------------------------------------------------------------------------------------------- 
def edit_franchisee_function(params):
    recived_data=get_franchisee_recieved_params(params)
    modified_data=get_franchisee_modified_params(recived_data)

    franchisee_obj=Franchisee.objects.get(id=recived_data["franchisee_id"])
    
    try:
        franchisee_detail=franchisee_obj.get_json()
        franchisee_detail.update(**modified_data)
        franchisee_save=Franchisee.objects.filter(id=recived_data["franchisee_id"]).update(**franchisee_detail)
        
    except Exception as e:
        print(e)
        return JsonResponse({"validation": " error while updating", "status": False})
    return JsonResponse({"validation": "done", "status": True})
# ------------------------------------------------------------------------------------------------------------------
