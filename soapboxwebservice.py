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
import base64
from soapbox.models import SoapboxAppusers ,SoapboxDevicetoken,SoapboxCategories,SoapboxConnectiontablesocialid

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
	
	
	#try:
		#received_json_data=json.loads(request.body)
		firstname= request.REQUEST['firstname']
		lastname=request.REQUEST['lastname']
		username=request.REQUEST['username']
		pwd=request.REQUEST['password']
		email=request.REQUEST['email']
		dateofbirth=request.REQUEST['dateofbirth']
		gender=request.REQUEST['gender']
		profileimage=request.REQUEST['profilepic']
		usertype=request.REQUEST['logintype']
		socialid = request.REQUEST['socialid']
		devicetype =request.REQUEST['devicetype']
		devicetoken = request.REQUEST['devicetoken']
		#phonenumber= request.REQUEST['phonenumber']

			
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
		# if(phonenumber ==''):
			# return HttpResponse(json.dumps({'message':'phonenumber is Missing.','success':0}))
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
				
				
				chkuserinfo=SoapboxAppusers.objects.get(email=email)
				if(usertype == '1'):
					socialsite_name ='facebook.com'
				if(usertype == '2'):
					socialsite_name ='twitter'
				if(usertype == '3'):
					socialsite_name ='google'
				if(usertype == '4'):
					socialsite_name ='linkedIn'
				
				updateValue ={"usertype":socialsite_name,"firstname": firstname,"lastname": lastname,"username":username,"socialid":socialid,"dateofbirth":dateofbirth,"gender":gender,"profilepic":imageurl}
				userSave=SoapboxAppusers.objects.filter(email=email).update(**updateValue)
				# try:
					# SoapboxConnectiontablesocialid.objects.get(socialid=socialid)
					# socialinfo={"userid":chkuserinfo.id,"socialid":socialid,"socialsitename": socialsite_name}
					# SoapboxConnectiontablesocialid.objects.filter(socialid=socialid).update(**socialinfo)
				# except SoapboxConnectiontablesocialid.DoesNotExist:
					# socialinfo=SoapboxConnectiontablesocialid(userid=chkuserinfo.id,socialid=socialid,socialsitename=socialsite_name)
					# socialinfo.save()
				
				if(devicetoken!='' and devicetype!=''):
					
					updateValue ={"devicetoken":devicetoken,"devicetype": devicetype}
					SoapboxDevicetoken.objects.filter(userid=chkuserinfo.id).update(**updateValue)
					userInfo={'socialsite_name':chkuserinfo.usertype,'apikey':chkuserinfo.apikey,'socialid':socialid,'userid':chkuserinfo.id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'profilepicurl':imageurl}
					return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
				else:
					userInfo={'socialsite_name':chkuserinfo.usertype,'apikey':chkuserinfo.apikey,'socialid':socialid,'userid':chkuserinfo.id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'profilepicurl':imageurl}
					return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
					
				
				
			
			except SoapboxAppusers.DoesNotExist:
				
				if(usertype == '1'):
					socialsite_name ='facebook.com'
				if(usertype == '2'):
					socialsite_name ='twitter'
				if(usertype == '3'):
					socialsite_name ='google'
				if(usertype == '4'):
					socialsite_name ='linkedIn'
				
				userSave=SoapboxAppusers(apikey=apikey,socialid=socialid,usertype=socialsite_name,firstname=firstname,lastname=lastname,username=username,email=email,dateofbirth=dateofbirth,gender=gender,created_at=nowTime,profilepic=imageurl)
				userSave.save()
				
				user_id=userSave.pk
				# socialinfo=SoapboxConnectiontablesocialid(userid=user_id,socialid=socialid,socialsitename=socialsite_name)
				# socialinfo.save()
				if(devicetoken!='' and devicetype!=''):
					userdevicetoken=SoapboxDevicetoken(userid=user_id,devicetype=devicetype,devicetoken=devicetoken)
					userdevicetoken.save()
					userInfo={'dateofbirth':dateofbirth,"socialsite_name":socialsite_name,'apikey':apikey,'socialid':socialid,'userid':user_id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'profilepicurl':imageurl}
					return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
				else:
					userInfo={'dateofbirth':dateofbirth,"socialsite_name":socialsite_name,'apikey':apikey,'socialid':socialid,'userid':user_id,'firstname':firstname,'lastname':lastname,'username':username,'email':email,'dateofbirth':dateofbirth,'gender':gender,'profilepicurl':imageurl}
					return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
				
				
		elif(usertype != 0 and socialid == '' ):
			return HttpResponse(json.dumps({'message':'SocialID is Missing.','success':0}))
		elif(usertype == 0 and socialid != '' ):
			return HttpResponse(json.dumps({'message':'Login Type incorrect.','success':0}))
		else:
			return HttpResponse(json.dumps({'message':'error.','success':0}))
	# except Exception as e:
		# return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		

	
	
	
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
					recArray['phonenumber']=userInfo.phonenumber
					
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

		
def channelSuggestions(request):
	try:
		channel_json_data=json.loads(request.body)
		#userid= channel_json_data['userid']
		channelname= channel_json_data['channelname']
		nowTime = datetime.datetime.now()
		records = []
		#if(userid==''):
			#return HttpResponse(json.dumps({'message':'userId is Missing.','success':0}))
		if(channelname==''):
			return HttpResponse(json.dumps({'message':'Channel name is Missing.','success':0}))
		if(channelname!=''):
			
			channelInfo=SoapboxCategories.objects.all().filter(channel_name__icontains=channelname)
			if channelInfo.exists():
				for channeldata in channelInfo.all(): 
					if(channeldata.type_of_channel==1):
						category='custom'
					else:
						category='static'
					
					arr={}
					arr['name'] = channeldata.channel_name
					arr['id'] = channeldata.id
					arr['created_at'] =str(channeldata.created_at)
					arr['modified_at'] =''
					arr['category'] =category
					records.append(arr)
					
				return HttpResponse(json.dumps({'message':'stored channel name','data':records}))
			else:
			
				return HttpResponse(json.dumps({'message':'No Result Found.','success':1}))
		else:
			error={'error':'invalid parameters'}
			return HttpResponse(json.dumps(error))
	
	except Exception as e:
	    return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))	
	
	#http://192.168.1.250:8080/addChannel/?channelname=&categoryname=
	# add category
	
def connectSocialMedia(request):
	try:
		connectSocialMedia_json_data=json.loads(request.body)
		records = []
		userid = connectSocialMedia_json_data['userid']
		socialid= connectSocialMedia_json_data['socialid']
		socialsitename = connectSocialMedia_json_data['socialsitename']
		if(userid == ''):
			return HttpResponse(json.dumps({'message':'userid is Missing.','success':0}))
		if(socialid == ''):
			return HttpResponse(json.dumps({'message':'socialid is Missing.','success':0}))
		if(socialsitename == ''):
			return HttpResponse(json.dumps({'message':'socialsitename is Missing.','success':0}))
		
		if(userid!='' and socialid!='' and socialsitename!=''):
			
			try:
				socialidinfo=SoapboxConnectiontablesocialid.objects.get(socialid=socialid,userid=userid)
				socialInfo=SoapboxConnectiontablesocialid.objects.all().filter(userid=userid)
				if socialInfo.exists():
					for socialInfos in socialInfo.all(): 
						recArray = {}
						recArray['userId']=socialInfos.userid
						recArray['socialid']=socialInfos.socialid
						recArray['socialsite_name']=socialInfos.socialsitename
						records.append(recArray)
					
					return HttpResponse(json.dumps({'message':'Already connected with Socialsite','success':1,'data':records}))
			
			except SoapboxConnectiontablesocialid.DoesNotExist:
				if(socialsitename == '1'):
					socialsite_name ='facebook.com'
				if(socialsitename == '2'):
					socialsite_name ='twitter'
				if(socialsitename == '3'):
					socialsite_name ='google'
				if(socialsitename == '4'):
					socialsite_name ='linkedIn'
				
				socialinfo=SoapboxConnectiontablesocialid(userid=userid,socialid=socialid,socialsitename=socialsite_name)
				userSave=socialinfo.save()
				#user_id=userSave.pk
				userInfo={"socialsite_name":socialsite_name,'socialid':socialid,'usreId':userid}
				return HttpResponse(json.dumps({'message':'connect with socialsite','success':1,'data':userInfo}))
		else:
			error={'error':'invalid parameters'}
			return HttpResponse(json.dumps(error))
	except Exception as e:
	    return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		
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
	
	
def uploadfile(request):



	profileimage = request.REQUEST['profileimage']
	if(profileimage!=''):
		nowTime = datetime.datetime.now()
		filename=  nowTime.strftime("%S%H%M%f")+'.jpg'
		b64data = profileimage.split(',') # [sic]
		out = open(settings.BASE_DIR+"/soapbox/profilepic/"+filename, "wb")
		out.write(decodestring(b64data))
		out.close()
		baseurl = request.build_absolute_uri('/')[:-6]
		imageurl= baseurl+"/soapbox/soapbox/profilepic/"+filename
		return HttpResponse(imageurl)
	else:
		imageurl='empty'
		return HttpResponse(imageurl)
		