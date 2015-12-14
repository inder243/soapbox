from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpRequest
from django.http import HttpResponse
from django import http
from django.conf import settings
from django.shortcuts import render_to_response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import redirect
from django import forms
from django.utils import timezone
import uuid
import md5, json, MySQLdb,simplejson
from django.core import serializers
from django.db.models import Q
import sys
import time
import string
import datetime

from soapbox.models import AppRegister, Users, PersonalDetails, UserStatus, UserImage, UserStatus, UserFollowers, Categories, GroupUsersCategory, Posts, PostCategories, PostLikes, PostListens, PostShares, Comments, PodcastTimer

# Create your views here.

def appRegister(request):
	
	firstname=request.REQUEST['firstname']
	lastname=request.REQUEST['lastname']
	username=request.REQUEST['username']
	pwd=request.REQUEST['password']
	email=request.REQUEST['email']
	dateofbirth=request.REQUEST['dateofbirth']
	gender=request.REQUEST['gender']
	profileimage=request.REQUEST['profilepic']
	
	password = md5.new(pwd).hexdigest()
	nowTime = datetime.datetime.now()
	filename=  nowTime.strftime("%S%H%M%f")+'.jpg'
	fh = open(settings.BASE_DIR+"/soapbox/profilepic/"+filename, "wb")
	fh.write(profileimage.decode('base64'))
	fh.close()
	
	baseurl = request.build_absolute_uri('/')[:-6]
	imageurl= baseurl+"/soapbox/soapbox/profilepic/"+filename

	
	if(firstname!='' and lastname!='' and username!='' and password!='' and dateofbirth!='' and email!='' and gender !=''):
	
		try:
			chkusr=AppRegister.objects.get(email=email)
			error ={'message':'Emailid already exist' ,'success': 0}
			return HttpResponse(json.dumps(error))
			
		except AppRegister.DoesNotExist:
			
			userSave=AppRegister(firstname=firstname,lastname=lastname,username=username,email=email,password=password,dateofbirth=dateofbirth,gender=gender,currentdate=nowTime,profilepic=imageurl)
			userSave.save()
			user_id=userSave.pk
			userInfo={'userid':user_id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'progilepicurl':imageurl}
			return HttpResponse(json.dumps({'message':'Registered successfully with Soapbox App.','success':1,'information':userInfo}))
		
	else:
		error ={'error':'invalid parameters'}
		return HttpResponse(json.dumps(error))
	
	
	
	#register webservice
	#http://192.168.1.250:8080/appregister/?profilepic=&firstname=&lastname=&username=&email=&dateofbirth=&password=&gender=
	
	
def appLogin(request):
	recArray ={}
	email = request.REQUEST['email']
	password = request.REQUEST['password']
	pwd = md5.new(password).hexdigest()
	if(email!='' and password!=''):
		try:
			userInfo=AppRegister.objects.get(email=email,password=pwd)
			recArray['userId']=userInfo.id
			recArray['email']=userInfo.email
			recArray['firstName']=userInfo.firstname
			recArray['lastName']=userInfo.lastname
			recArray['userName']=userInfo.username
			recArray['gender']=userInfo.gender
			recArray['profileUrl']=userInfo.profilepic
			
			
			return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':recArray}))
			
		except AppRegister.DoesNotExist:
			return HttpResponse(json.dumps({'message':'Email or Password incorrect.','success':0}))
	else:
		error={'error':'invalid parameters'}
		return HttpResponse(json.dumps(error))
		
		#login webservice 
		#http://192.168.1.250:8080/applogin/?email=&password=
	
	
	