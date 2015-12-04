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
from django.core.serializers.json import DjangoJSONEncoder
import md5, json, MySQLdb,simplejson
from django.core import serializers
from django.db.models import Q
import sys
import time
import string
import datetime
import re

from soapbox.models import SoapboxAppusers ,SoapboxDevicetoken

# Create your views here.

def appRegister(request):
	# received_json_data=json.loads(request.body)
	# return HttpResponse(received_json_data['firstname'])
	# firstname= request.REQUEST.get('firstname', None)
	# lastname=request.REQUEST.get('lastname', None)
	# username=request.REQUEST.get('username', None)
	# pwd=request.REQUEST.get('password', None)
	# email=request.REQUEST.get('email', None)
	# dateofbirth=request.REQUEST.get('dateofbirth', None)
	# gender=request.REQUEST.get('gender', None)
	# profileimage=request.REQUEST.get('profileimage', None)
	# usertype=request.REQUEST.get('logintype', None)
	# socialid = request.REQUEST.get('socialid', None) 
	# devicetype =request.REQUEST.get('devicetype', None)
	# devicetoken = request.REQUEST.get('devicetoken', None)
	
	
	try:
		received_json_data=json.loads(request.body)
		
		firstname= received_json_data['firstname']
		lastname=received_json_data['lastname']
		
		username=received_json_data['username']
		
		pwd=received_json_data['password']
		email=received_json_data['email']
		dateofbirth=received_json_data['dateofbirth']
		gender=received_json_data['gender']
		profileimage=received_json_data['profilepic']
		usertype=received_json_data['logintype']
		socialid = received_json_data['socialid']
		devicetype =received_json_data['devicetype']
		devicetoken = received_json_data['devicetoken']

			
		if(firstname == ''):
			return HttpResponse(json.dumps({'message':'Firstname is Missing.','success':0}))
		if(lastname ==''):
			return HttpResponse(json.dumps({'message':'Lastname is Missing.','success':0}))
		if(username ==''): 
			return HttpResponse(json.dumps({'message':'Username is Missing.','success':0}))
		if(dateofbirth ==''): 
			return HttpResponse(json.dumps({'message':'Dateofbirth Missing.','success':0}))
		if(email ==''):
			return HttpResponse(json.dumps({'message':'Email is Missing.','success':0}))
		if(gender ==''): 
			return HttpResponse(json.dumps({'message':'Gender is Missing.','success':0}))
		# if(devicetype == ''):
			# return HttpResponse(json.dumps({'message':'devicetype is Missing.','success':0}))
		# if(devicetoken == ''):
			# return HttpResponse(json.dumps({'message':'devicetoken is Missing.','success':0}))
		if(usertype ==''):
			return HttpResponse(json.dumps({'message':'Usertype is Missing.','success':0}))
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == '':
			return HttpResponse(json.dumps({'message':'Invalid email.','success':0}))
		
		
		nowTime = datetime.datetime.now()
		apikey = md5.new(nowTime.strftime("%d%f%M%H%S")).hexdigest()
		if(profileimage!=''):
			
			filename=  nowTime.strftime("%S%H%M%f")+'.jpg'
			fh = open(settings.BASE_DIR+"/soapbox/profilepic/"+filename, "wb")
			fh.write(profileimage.decode('base64'))
			fh.close()

			baseurl = request.build_absolute_uri('/')[:-6]
			imageurl= baseurl+"/soapbox/soapbox/profilepic/"+filename
		else:
			imageurl=''
			
		if(pwd != '' and usertype ==0 and socialid == ''):
			#return HttpResponse('a')
			try:
			
				chkusr=SoapboxAppusers.objects.get(email=email,usertype='appuser')
				error ={'message':'Emailid already exist' ,'success': 0}
				return HttpResponse(json.dumps(error))
				
			except SoapboxAppusers.DoesNotExist:
				
				userSave=SoapboxAppusers(apikey=apikey,usertype='appuser',firstname=firstname,lastname=lastname,username=username,email=email,password=md5.new(pwd).hexdigest(),dateofbirth=dateofbirth,gender=gender,created_at=nowTime,profilepic=imageurl)
				userSave.save()
				user_id=userSave.pk
			if(devicetoken!='' and devicetype!=''):
				try:
					chkdevicetoken=SoapboxDevicetoken.objects.get(userid=user_id,devicetoken=devicetoken)
					updateValue ={"devicetoken":devicetoken,"devicetype": devicetype}
					SoapboxDevicetoken.objects.filter(userid=user_id).update(**updateValue)
				except SoapboxDevicetoken.DoesNotExist:
					userdevicetoken=SoapboxDevicetoken(userid=user_id,devicetype=devicetype,devicetoken=devicetoken)
					userdevicetoken.save()
				userInfo={'site_name':'appuser','apikey':apikey,'userid':user_id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'profilepicurl':imageurl}
				return HttpResponse(json.dumps({'message':'Registered successfully with Soapbox App.','success':1,'information':userInfo}))
			else:
				userInfo={'site_name':'appuser','apikey':apikey,'userid':user_id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'profilepicurl':imageurl}
				return HttpResponse(json.dumps({'message':'Registered successfully with Soapbox App.','success':1,'information':userInfo}))
		
		
		elif (socialid != '' and usertype != 0):
			
			try:
				chkuserinfo=SoapboxAppusers.objects.get(socialid=socialid)
				
				updateValue ={"firstname": firstname,"lastname": lastname,"username":username,"email":email,"dateofbirth":dateofbirth,"gender":gender,"profilepic":imageurl}
				userSave=SoapboxAppusers.objects.filter(socialid=socialid).update(**updateValue)
				updateValue ={"devicetoken":devicetoken,"devicetype": devicetype}
				SoapboxDevicetoken.objects.filter(userid=chkuserinfo.id).update(**updateValue)
				
				userInfo={'socialsite_name':chkuserinfo.usertype,'apikey':chkuserinfo.apikey,'socialid':socialid,'userid':chkuserinfo.id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'profilepicurl':imageurl}
				return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
			
			except SoapboxAppusers.DoesNotExist:
				
				if(usertype == 1):
					socialsite_name ='facebook.com'
				if(usertype == 2):
					socialsite_name ='twitter'
				if(usertype == 3):
					socialsite_name ='google'
				if(usertype == 4):
					socialsite_name ='linkedIn'
				
				userSave=SoapboxAppusers(apikey=apikey,socialid=socialid,usertype=socialsite_name,firstname=firstname,lastname=lastname,username=username,email=email,dateofbirth=dateofbirth,gender=gender,created_at=nowTime,profilepic=imageurl)
				userSave.save()
				
				user_id=userSave.pk
				userdevicetoken=SoapboxDevicetoken(userid=user_id,devicetype=devicetype,devicetoken=devicetoken)
				userdevicetoken.save()
			
				
				userInfo={'dateofbirth':dateofbirth,"socialsite_name":socialsite_name,'apikey':apikey,'socialid':socialid,'userid':user_id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'profilepicurl':imageurl}
				
				return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
				
				
		elif(usertype != 0 and socialid == '' ):
			return HttpResponse(json.dumps({'message':'SocialID is Missing.','success':0}))
		elif(usertype == 0 and socialid != '' ):
			return HttpResponse(json.dumps({'message':'Login Type incorrect.','success':0}))
		else:
			return HttpResponse(json.dumps({'message':'error.','success':0}))
	except Exception as e:
		return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		

	
	
	
	#register webservice
	#http://192.168.1.250:8080/appregister/?profilepic=&firstname=&lastname=&username=&email=&dateofbirth=&password=&gender=
	
	
def appLogin(request):
		try:
			recArray ={}

			login_json_data=json.loads(request.body)
			email = login_json_data['email']
			password = login_json_data['password']
			devicetype = login_json_data['devicetype']
			devicetoken = login_json_data['devicetoken']
		
			if(email == ''):
				return HttpResponse(json.dumps({'message':'email is Missing.','success':0}))
			if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == '':
				return HttpResponse(json.dumps({'message':'Invalid email.','success':0}))
			if(devicetype == ''):
				return HttpResponse(json.dumps({'message':'devicetype is Missing.','success':0}))
			if(devicetoken == ''):
				return HttpResponse(json.dumps({'message':'devicetoken is Missing.','success':0}))
			if(password == ''):
				return HttpResponse(json.dumps({'message':'password is Missing.','success':0}))

			
			if(password != '' and email !='' and devicetoken!= '' and devicetype!=''):
			
				try:
					userInfo=SoapboxAppusers.objects.get(email=email,password=md5.new(password).hexdigest(),usertype='appuser')
					recArray['userId']=userInfo.id
					recArray['apikey']=userInfo.apikey
					recArray['email']=userInfo.email
					recArray['firstName']=userInfo.firstname
					recArray['lastName']=userInfo.lastname
					recArray['userName']=userInfo.username
					recArray['gender']=userInfo.gender
					recArray['profileUrl']=userInfo.profilepic
					recArray['dateofbirth']=str(userInfo.dateofbirth)
					recArray['site_name']=userInfo.usertype
					
					
					try:
						userdeviceInfo= SoapboxDevicetoken.objects.get(userid=SoapboxAppusers.objects.get(email=email,usertype='appuser').id)
										
						return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':recArray}))
						
					except SoapboxDevicetoken.DoesNotExist:
						return HttpResponse(json.dumps({'message':'User does not exist with this Devicetoken .','success':0}))
				except SoapboxAppusers.DoesNotExist:
						return HttpResponse(json.dumps({'message':'Incorrect email and password.','success':0}))
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error))
		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
			
		#login webservice 
		#http://192.168.1.250:8080/applogin/?email=&password=&devicetoken=&devicetype=
		
		
		
		
def addCategory(request):
	channelname = request.REQUEST['channelname']
	categoryname = request.REQUEST['categoryname']
	
	if(categoryname!='' and channelname!=''):
		try:
			userInfo=AppCategory.objects.get(category=categoryname,channel=channelname)
			
			return HttpResponse(json.dumps({'message':'channel name already exit.','success':0}))
			
		except AppCategory.DoesNotExist:
			channelSave=AppCategory(category=categoryname,channel=channelname)
			channelSave.save()
			user_id=channelSave.pk
			categoryInfo={'userid':user_id,'category':categoryname,'channel':channelname}
			return HttpResponse(json.dumps({'message':'channel add successfully.','success':1,'category':categoryInfo}))
	else:
		error={'error':'invalid parameters'}
		return HttpResponse(json.dumps(error))
	
	#http://192.168.1.250:8080/addcategory/?channelname=&categoryname=
	# add category
	
def serachCategory(request):

	channelname = request.REQUEST['channelname']
	if(channelname!=''):
		try:
			channelinfo = AppCategory.objects.all().filter(channel__icontains=channelname)
			
			return HttpResponse(serializers.serialize('json', channelinfo, fields=('channel')))
		except AppCategory.DoesNotExist:
			return HttpResponse(json.dumps({'message':'No Result Found .','success':0}))
	
	else:
		error={'error':'invalid parameters'}
		return HttpResponse(json.dumps(error))
		
	#http://192.168.1.250:8080/serachcategory/?channelname=