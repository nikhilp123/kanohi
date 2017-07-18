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


