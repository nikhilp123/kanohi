import os, re, datetime, json, uuid
from kanohi.settings import BASE_DIR, DEBUG
from kanohi_app.models import *

# from kanohi_app.views import  *


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

    user_obj = User()
    user_obj.username = username
    user_obj.set_password(str(params.get('password')))
    user_obj.save()
    user_id=user_obj.id
    data , massage , status = validate_user(params,user_id)
    if status:
        try:
            personal_info= UserDetails.objects.create(**data)
            print(personal_info)
            return JsonResponse({"validation": massage, "status": status})
        except Exception as e:
            print(e)    
            return JsonResponse({"validation": 'inconsistence data'})
    else:
        return JsonResponse({"validation": massage, "status": status})
#----------------------------------------------------------------------------------------------------------------------- 
def change_password_function(params):
    user=request.user
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