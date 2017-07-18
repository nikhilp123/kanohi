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

def get_recieved_params(params):
    kwargs={
        "franchisee_id":params.get("franchisee_id"),
        "franchisee_name":params.get("franchisee_name"),
        "owner_first_name":params.get("owner_first_name"),
        "owner_last_name":params.get("owner_last_name"),
        "owner_mob_number":params.get("owner_mob_number"),
        "owner_email":params.get("owner_email"),
        "subscription_start_date":params.get("subscription_start_date"),
        "subscription_end_date":params.get("subscription_end_date"),
        "address_line_one":params.get("address_line_one"),
        "address_line_two":params.get("address_line_two"),
        "city":params.get("city"),
        "state":params.get("state"),
        "pincode":params.get("pincode"),
        "is_active":params.get("is_active")}
    return kwargs

def get_modified_params(recived_data):
    kwargs={"franchisee_name" :recived_data["franchisee_name"],
        "owner_first_name":recived_data["owner_first_name"],
        "owner_last_name":recived_data["owner_last_name"],
        "owner_mob_number":recived_data["owner_mob_number"],
        "owner_email":recived_data["owner_email"],
        "subscription_start_date":convert_epoch_to_date(recived_data["subscription_start_date"]),
        "subscription_end_date":convert_epoch_to_date(recived_data["subscription_end_date"]),
        "address_line_one":recived_data["address_line_one"],
        "address_line_two":recived_data["address_line_two"],
        "city":recived_data["city"],
        "state":recived_data["state"],
        "pincode":recived_data["pincode"],
        "is_active":recived_data["is_active"]}
    return kwargs        

def get_users_recieved_params(params):
    kwargs={ "user_id":params.get("user_id"), 
    "first_name":params.get("first_name"),
    "last_name":params.get("last_name"),
    "mob_number":params.get("mob_number"),
    "email":params.get("email"),
    "franchisee_id":params.get("franchisee_id"),
    "role":params.get("role"),
    "is_active":params.get("is_active")}
    return kwargs 

def get_users_modified_params(recived_data):
    kwargs={"first_name" :recived_data["first_name"],
        "last_name" :recived_data["last_name"],
        "mob_number" :recived_data["mob_number"],
        "email" :recived_data["email"],
        "franchisee" :recived_data["franchisee_id"],
        "role" :recived_data["role"],
        "is_active" :recived_data["is_active"]}
    return kwargs

