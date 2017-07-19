# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# -------------------------------------------------------------------------------------------------------
# Create your models here.

def convert_date_to_epoch(date):
    return int(date.strftime('%s'))*1000 if date else None
# --------------------------------------------------------------------------------------------------------

class Franchisee(models.Model):
	franchisee_name=models.CharField(max_length=50)
	owner_first_name=models.CharField(max_length=50)		
	owner_last_name=models.CharField(max_length=50)		
	owner_mob_number=models.CharField(max_length=10)
	owner_email=models.EmailField()
	subscription_start_date=models.DateField()
	subscription_end_date=models.DateField()
	address_line_one=models.CharField(max_length=150)
	address_line_two=models.CharField(max_length=150)
	city=models.CharField(max_length=50)
	state=models.CharField(max_length=50)
	pincode=models.CharField(max_length=50)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return u'%s'%(self.franchisee_name)

	def get_json(self):	
		result={}
		result["franchisee_name"]=self.franchisee_name
		result["owner_first_name"]=self.owner_first_name
		result["owner_last_name"]=self.owner_last_name
		result["owner_mob_number"]=self.owner_mob_number
		result["owner_email"]=self.owner_email
		result["subscription_start_date"]=convert_date_to_epoch(self.subscription_start_date) if self.subscription_start_date else None
		result["subscription_end_date"]=convert_date_to_epoch(self.subscription_end_date) if self.subscription_end_date else None
		result["address_line_one"]=self.address_line_one
		result["address_line_two"]=self.address_line_two
		result["city"]=self.city
		result["state"]=self.state
		result["pincode"]=self.pincode
		result["is_active"]=self.is_active
		return result
#-------------------------------------------------------------------------------------------------------------------------------------------------- 

class UserDetails(models.Model):
	DOCTOR = 1
	LAB_ASSISTANCE = 2
	FRONT_DESK = 3
	FRANCHISEE_ADMIN = 4
	KANOHI_ADMIN = 5

	ROLE = (
	    (DOCTOR, 'Doctor'),
	    (LAB_ASSISTANCE, 'Lab assistance'),
	    (FRONT_DESK, 'Front desk'),
	    (FRANCHISEE_ADMIN, 'Franchisee admin'),
	    (KANOHI_ADMIN, 'Kanohi admin')
	)

	user =models.OneToOneField(User)
	first_name=models.CharField(max_length=50)		
	last_name=models.CharField(max_length=50)		
	mob_number=models.CharField(max_length=10)
	email=models.EmailField()
	franchisee=models.ForeignKey(Franchisee,null=True)		 	
	role=models.CharField(choices=ROLE,max_length=1, null=True)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return u'%s,%s'%(self.first_name,self.last_name)	

	def get_json(self):
		result={}
		result["user_id"]=self.id
		# result["user"]=self.user
		result["first_name"]=self.first_name
		result["last_name"]=self.last_name
		result["mob_number"]=self.mob_number
		result["email"]=self.email
		result["franchisee"]=self.franchisee.get_json() if self.franchisee else None
		result["is_active"]=self.is_active

		return result
# ----------------------------------------------------------------------------------------------------------------------------------


