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
from django.db.models import Q,Count,Sum
import sys
import time
import string
import datetime
import re
import base64
from soapbox.models import SoapboxAppusers ,SoapboxDevicetoken,SoapboxCategories,SoapboxConnectiontablesocialid,SoapboxSubscribechannel,SoapboxPosts,SoapboxPostlikeandshare,SoapboxUserfollowers

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
		received_json_data=json.loads(request.body)
		
		firstname= received_json_data['first_name']
		lastname=received_json_data['last_name']
		
		username=received_json_data['username']
		
		pwd=received_json_data['password']
		email=received_json_data['email']
		dateofbirth=received_json_data['dob']
		gender=received_json_data['gender']
		profileimage=received_json_data['profile_pic']
		usertype=received_json_data['login_type']
		socialid = received_json_data['social_id']
		devicetype =received_json_data['device_type']
		devicetoken = received_json_data['device_id']
		intro_audio_url = received_json_data['intro_audio_url']

			
		if(firstname == ''):
			return HttpResponse(json.dumps({'message':'Firstname is Missing.','success':0}))
		if(lastname ==''):
			return HttpResponse(json.dumps({'message':'Lastname is Missing.','success':0}))
		if(username ==''): 
			return HttpResponse(json.dumps({'message':'Username is Missing.','success':0}))
		if(dateofbirth ==''): 
			return HttpResponse(json.dumps({'message':'Dateofbirth Missing.','success':0}))
		if(email =='' and usertype ==0):
			return HttpResponse(json.dumps({'message':'Email is Missing.','success':0}))
		#if(gender ==''): 
			#return HttpResponse(json.dumps({'message':'Gender is Missing.','success':0}))
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
				
				userSave=SoapboxAppusers(intro_audio_url=intro_audio_url,apikey=apikey,usertype='appuser',firstname=firstname,lastname=lastname,username=username,email=email,password=md5.new(pwd).hexdigest(),dateofbirth=dateofbirth,gender=gender,created_at=nowTime,profilepic=imageurl)
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
				userInfo={'intro_audio_url':intro_audio_url,'site_name':'appuser','apikey':apikey,'user_id':user_id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
				return HttpResponse(json.dumps({'message':'Registered successfully with Soapbox App.','success':1,'information':userInfo}))
			else:
				userInfo={'intro_audio_url':intro_audio_url,'site_name':'appuser','apikey':apikey,'user_id':user_id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
				return HttpResponse(json.dumps({'message':'Registered successfully with Soapbox App.','success':1,'information':userInfo}))
		
		
		elif (socialid != '' and usertype != 0):
			
			try:
				chkuserinfo=SoapboxAppusers.objects.get(socialid=socialid)
				
			
				updateValue ={"intro_audio_url":intro_audio_url,"firstname": firstname,"lastname": lastname,"username":username,"email":email,"dateofbirth":dateofbirth,"gender":gender,"profilepic":imageurl}
				userSave=SoapboxAppusers.objects.filter(socialid=socialid).update(**updateValue)
				if(devicetoken!='' and devicetype!=''):
					updateValue ={"devicetoken":devicetoken,"devicetype": devicetype}
					SoapboxDevicetoken.objects.filter(userid=chkuserinfo.id).update(**updateValue)
					
					userInfo={'intro_audio_url':chkuserinfo.intro_audio_url,'socialsite_name':chkuserinfo.usertype,'apikey':chkuserinfo.apikey,'social_id':socialid,'user_id':chkuserinfo.id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
					return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
				else:
					userInfo={"intro_audio_url":intro_audio_url,'socialsite_name':chkuserinfo.usertype,'apikey':chkuserinfo.apikey,'social_id':socialid,'user_id':chkuserinfo.id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
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
				
				userSave=SoapboxAppusers(intro_audio_url=intro_audio_url,apikey=apikey,socialid=socialid,usertype=socialsite_name,firstname=firstname,lastname=lastname,username=username,email=email,dateofbirth=dateofbirth,gender=gender,created_at=nowTime,profilepic=imageurl)
				userSave.save()
				
				user_id=userSave.pk
				if(devicetoken!='' and devicetype!=''):
					userdevicetoken=SoapboxDevicetoken(userid=user_id,devicetype=devicetype,devicetoken=devicetoken)
					userdevicetoken.save()
					userInfo={"intro_audio_url":intro_audio_url,'dob':dateofbirth,"socialsite_name":socialsite_name,'apikey':apikey,'social_id':socialid,'user_id':user_id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
					return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
				else:
					userInfo={"intro_audio_url":intro_audio_url,'dateofbirth':dateofbirth,"socialsite_name":socialsite_name,'apikey':apikey,'social_id':socialid,'user_id':user_id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dof':dateofbirth,'gender':gender,'profile_pic':imageurl}
					return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
				
		elif(usertype != 0 and socialid == '' ):
			return HttpResponse(json.dumps({'message':'Social_id is Missing.','success':0}))
		elif(usertype == 0 and socialid != '' ):
			return HttpResponse(json.dumps({'message':'Login Type incorrect.','success':0}))
		else:
			return HttpResponse(json.dumps({'message':'error.','success':0}))
	#except Exception as e:
		#return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		

	
	
	
	#register webservice
	#http://192.168.1.250:8080/appregister/?profilepic=&firstname=&lastname=&username=&email=&dateofbirth=&password=&gender=
	
	
def appLogin(request):
	
	try:
		recArray ={}

		login_json_data=json.loads(request.body)
		email = login_json_data['email']
		password = login_json_data['password']
		devicetype = login_json_data['device_type']
		devicetoken = login_json_data['device_id']
	
		if(email == ''):
			return HttpResponse(json.dumps({'message':'email is Missing.','success':0}))
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == '':
			return HttpResponse(json.dumps({'message':'Invalid email.','success':0}))
		# if(devicetype == ''):
			# return HttpResponse(json.dumps({'message':'devicetype is Missing.','success':0}))
		# if(devicetoken == ''):
			# return HttpResponse(json.dumps({'message':'devicetoken is Missing.','success':0}))
		if(password == ''):
			return HttpResponse(json.dumps({'message':'password is Missing.','success':0}))

		if(password != '' and email !='' ):
		
			try:
				userInfo=SoapboxAppusers.objects.get(email=email,password=md5.new(password).hexdigest(),usertype='appuser')
				recArray['user_id']=userInfo.id
				recArray['apikey']=userInfo.apikey
				recArray['email']=userInfo.email
				recArray['first_name']=userInfo.firstname
				recArray['last_name']=userInfo.lastname
				recArray['username']=userInfo.username
				recArray['gender']=userInfo.gender
				recArray['profile_pic']=userInfo.profilepic
				recArray['dob']=str(userInfo.dateofbirth)
				recArray['site_name']=userInfo.usertype
				#recArray['phonenumber']=userInfo.phonenumber
				recArray['intro_audio_url']=userInfo.intro_audio_url
				
				if(devicetoken!='' and devicetype!=''):
					try:
						userdeviceInfo= SoapboxDevicetoken.objects.get(userid=SoapboxAppusers.objects.get(email=email,usertype='appuser').id)
										
						return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':recArray}))
						
					except SoapboxDevicetoken.DoesNotExist:
						return HttpResponse(json.dumps({'message':'User does not exist with this Devicetoken .','success':0}))
				return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':recArray}))		
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
	headervalue = headerinfo(request);
	
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key is incorrect.','success':0}))
	else:
		try:
			channel_json_data=json.loads(request.body)
			userid= channel_json_data['user_id']
			channelname=channel_json_data['channel_name']
			nowTime = datetime.datetime.now()
			records = []
			if(userid==''):
				return HttpResponse(json.dumps({'message':'userId is Missing.','success':0}))
			if(channelname==''):
				return HttpResponse(json.dumps({'message':'Channel name is Missing.','success':0}))
			if(userid!='' and channelname!=''):
				
				channelInfo=SoapboxCategories.objects.all().filter(channel_name__icontains=channelname)
				if channelInfo.exists():
					for channeldata in channelInfo.all(): 
						arr={}
						arr['channel_name'] = channeldata.channel_name
						arr['channel_id'] = channeldata.id
						records.append(arr)
						
					return HttpResponse(json.dumps({'message':'stored channel name','channel_name':records,'success':1}))
				else:
				
					#channelSave=SoapboxCategories(created_by_id=userid,channel_name=channelname,created_at=nowTime,type_of_channel=1)
					#channelSave.save()
					#user_id=channelSave.pk
					#categoryInfo={'userid':user_id,'channel':channelname}
					#return HttpResponse(json.dumps({'message':'channel add successfully.','success':1,'category':categoryInfo}))
					return HttpResponse(json.dumps({'message':'No Result Found.','success':0}))
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error))
		
		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))	
	
	#http://192.168.1.250:8080/addChannel/?channelname=&categoryname=
	# add category
	

def connectSocialMedia(request):
	headervalue = headerinfo(request);
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key is incorrect.','success':0}))
	else:
		try:
			connectSocialMedia_json_data=json.loads(request.body)
			records = []
			userid = connectSocialMedia_json_data['user_id']
			socialid= connectSocialMedia_json_data['social_id']
			socialsitename = connectSocialMedia_json_data['social_site_name']
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
					userInfo={"socialsite_name":socialsite_name,'social_id':socialid,'usre_id':userid}
					return HttpResponse(json.dumps({'message':'connect with socialsite','success':1,'data':userInfo}))
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error))
		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		
		
		
		
def subscribechannel(request):
	headervalue = headerinfo(request);
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key is incorrect.','success':0}))
	else:
		try:
			subscribechannel_json_data=json.loads(request.body)
			recArray={}
			userid = subscribechannel_json_data['user_id']
			channel_id = subscribechannel_json_data['channel_id']
			issubscribe = subscribechannel_json_data['is_subscribe']
			if(userid == ''):
				return HttpResponse(json.dumps({'message':'userid is Missing.','success':0}))
			if(channel_id == ''):
				return HttpResponse(json.dumps({'message':'channel_id is Missing.','success':0}))
			if(issubscribe == ''):
				return HttpResponse(json.dumps({'message':'isSubscribe flag is Missing.','success':0}))

				
			if(userid !='' and channel_id!='' and issubscribe!=''):
				try:
					socialidinfo=SoapboxSubscribechannel.objects.get(channelid=channel_id,userid=userid)
					# recArray['channelid']=socialidinfo.channelid
					# recArray['userid']=socialidinfo.userid
					#recArray['issubscribe']=socialidinfo.issubscribe
					if(issubscribe =='1'):
						updateValue ={"issubscribe":issubscribe}
						SoapboxSubscribechannel.objects.filter(userid=userid,channelid=channel_id).update(**updateValue)
						return HttpResponse(json.dumps({'success':1,'message':'Channel Subscribed successfully '}))
					else:
						updateValue ={"issubscribe":issubscribe}
						SoapboxSubscribechannel.objects.filter(userid=userid,channelid=channel_id).update(**updateValue)
						return HttpResponse(json.dumps({'success':0,'message':'Channel Unsubscribed successfully'}))
					
				except SoapboxSubscribechannel.DoesNotExist:
					channelsubscribe=SoapboxSubscribechannel(userid=userid,channelid=channel_id,issubscribe=issubscribe)
					channelsubscribe.save()
					
					return HttpResponse(json.dumps({'success':1,'message':'Channel Subscribed successfully'}))
				
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error))
		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
	
	#http://192.168.1.250:8080/subscribechannel/?channelname=&categoryname=
	
	
		
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
	try:
		audio_json_data=json.loads(request.body)
		rawdata = audio_json_data['raw_data']
		extension = audio_json_data['extension']
		type = audio_json_data['type']
		if(rawdata == ''):
			return HttpResponse(json.dumps({'message':'Data is Missing.','success':0}))
		if(extension == ''):
			return HttpResponse(json.dumps({'message':'Extension is Missing.','success':0}))
		if(type == ''):
			return HttpResponse(json.dumps({'message':'Type is Missing.','success':0}))

		nowTime = datetime.datetime.now()
		if(type == '1'):
			filename=  nowTime.strftime("%S%H%M%f")+'.'+extension
			fh = open(settings.BASE_DIR+"/soapbox/audiofile/"+filename, "wb")
			fh.write(rawdata.decode('base64'))
			fh.close()
			baseurl = request.build_absolute_uri('/')[:-6]
			audiourl= baseurl+"/soapbox/soapbox/audiofile/"+filename
			return HttpResponse(json.dumps({'audio_url':audiourl,'success':1}))	
		elif(type == '2'):
			filename=  nowTime.strftime("%S%H%M%f")+'.'+extension
			fh = open(settings.BASE_DIR+"/soapbox/profilepic/"+filename, "wb")
			fh.write(rawdata.decode('base64'))
			fh.close()
			baseurl = request.build_absolute_uri('/')[:-6]
			imageurl= baseurl+"/soapbox/soapbox/profilepic/"+filename
			return HttpResponse(json.dumps({'image_url':imageurl,'success':1}))	
		else:
			return HttpResponse(json.dumps({'message':'Incorrect format type.','success':0}))	
		
			
	
	except Exception as e:
		return HttpResponse(json.dumps({'message':e,'success':0}))
		
		
		
def postAudioMessage(request):
	headervalue = headerinfo(request);
	
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key is incorrect.','success':0}))
	else:
		try:
			records = []
			nowTime = datetime.datetime.now()
			posted_on=nowTime.strftime("%Y-%m-%d")
			posted_at=nowTime.strftime("%H:%M:%S")
			postaudio_json_data = json.loads(request.body)

			userid = postaudio_json_data['user_id']
			audiofile = postaudio_json_data['audiofile']
			title = postaudio_json_data['title']
			if(userid == ''):
				return HttpResponse(json.dumps({'message':'userid is Missing.','success':0}))
			if(audiofile == ''):
				return HttpResponse(json.dumps({'message':'audiofile is Missing.','success':0}))
			if(title == ''):
				return HttpResponse(json.dumps({'message':'title is Missing.','success':0}))
			
			post_json_data=json.loads(request.body)
			jsonData = post_json_data["hashtags"]
			for item in jsonData:
					
				channelinfos = SoapboxCategories.objects.all().filter(channel_name= item.get("hash_tag_name"),id =item.get("id"))
				
				if channelinfos.exists():
					post=SoapboxPosts(userid=userid,post_title=title,post_file_url=audiofile,posted_on=nowTime,posted_at=posted_at,channelid=item.get("id"),channel_name=item.get("hash_tag_name"))
					post.save()
					post_id = str(post.pk)
					recArray={"id":post_id,"post_title":title,"post_file_url":audiofile,"posted_on":posted_on,"posted_at":posted_at,"user_by_id":userid,"hash_tag_id":item.get("id"),"hash_tag_name":item.get("hash_tag_name")}
					records.append(recArray)
					
				else:
					
					channelSave=SoapboxCategories(created_by_id=userid,channel_name=item.get("hash_tag_name"),created_at=nowTime,type_of_channel=1)
					channelSave.save()
					channel_id=channelSave.pk
					post=SoapboxPosts(userid=userid,post_title=title,post_file_url=audiofile,posted_on=nowTime,posted_at=posted_at,channelid=channel_id,channel_name=item.get("hash_tag_name"))
					post.save()
					post_id = str(post.pk)
					recArray={"id":post_id,"post_title":title,"post_file_url":audiofile,"posted_on":posted_on,"posted_at":posted_at,"user_by_id":userid,"hash_tag_id":channel_id,"hash_tag_name":item.get("hash_tag_name")}
					records.append(recArray)
			return HttpResponse(json.dumps({"success": 1,'message':'save successfully','data':records}))
			

		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		
		
		
		
		
		
def follow(request):
	headervalue = headerinfo(request);
	
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
		try:
			follow_json_data=json.loads(request.body)
			userid = follow_json_data['user_id']
			following_user_id = follow_json_data['following_user_id']
			if(userid == ''):
				return HttpResponse(json.dumps({'message':'userid is Missing.','success':'0'}))
			if(following_user_id ==''):
				return HttpResponse(json.dumps({'message':'following_user_id is Missing.','success':'0'}))
			
			if(userid !='' and following_user_id!='' ):
			
				try:
					followuser = SoapboxUserfollowers.objects.get(user_id=userid,following_user_id=following_user_id)
					SoapboxUserfollowers.objects.filter(user_id=userid,following_user_id=following_user_id).delete()
					return HttpResponse(json.dumps({"success":0,"message": "user unfollow successfully."}))
				
				except SoapboxUserfollowers.DoesNotExist:
					follow=SoapboxUserfollowers(following_user_id=following_user_id,user_id=userid)
					follow.save()
					return HttpResponse(json.dumps({"success":1,"message": "followed successfully."}))
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error))
		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
	
	
	
def	postAudioReplyMessage(request):
	headervalue = headerinfo(request);
	
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
			
		try: 
			postaudio_json_data=json.loads(request.body)
			matter_msg_id = postaudio_json_data['matter_msg_id']
			userid = postaudio_json_data['user_id']
			audiofile = postaudio_json_data['audiofile']
			nowTime = datetime.datetime.now()
			if(userid == ''):
				return HttpResponse(json.dumps({'message':'userid is Missing.','success':'0'}))
			if(matter_msg_id ==''):
				return HttpResponse(json.dumps({'message':'matter_msg_id is Missing.','success':'0'}))
			if(audiofile ==''):
				return HttpResponse(json.dumps({'message':'audiofile is Missing.','success':'0'}))
				
			if(userid !='' and matter_msg_id!='' and audiofile!=''):
				posted_on=nowTime.strftime("%Y-%m-%d")
				posted_at=nowTime.strftime("%H:%M:%S")
				post=SoapboxPosts(userid=userid,post_file_url=audiofile,posted_on=posted_on,posted_at=posted_at,matter_msg_id=matter_msg_id,channelid=0,channel_name="")
				post.save()
				post_id = str(post.pk)
				data={"user_by_id": userid,"post_file_url":audiofile,"posted_on":posted_on,"posted_at":posted_at,"id":post_id}
				return HttpResponse(json.dumps({"success":1,"message": "save successfully."}))
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error)) 
			
		except Exception as e:
			return HttpResponse(json.dumps({'message':e,'success':0}))
			
			
			
			
def userPostList(request):
	headervalue = headerinfo(request);
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
			
		try: 
			records = []
		
			pickup_dict = []
			userPostList_json_data=json.loads(request.body)
			userid = userPostList_json_data['user_id']
			
			if(userid == ''):
				return HttpResponse(json.dumps({'message':'userid is Missing.','success':'0'}))
			

		

			userPostInfo=SoapboxPosts.objects.all().filter(userid=userid)
			#userPostInfo=SoapboxPosts.objects.all().filter(userid=userid).values_list('post_file_url').distinct()
			if userPostInfo.exists():
				for userPostInfos in userPostInfo.all(): 
					rec =[]
					recArray = {}
					
					chkusr=SoapboxAppusers.objects.get(id=userid)
					userrec ={}
					recArray['username']=chkusr.username
					recArray['profilepic']=chkusr.profilepic
					#recArray['likes']=0
					recArray['listen_count']=0
					#recArray['share_count']=0
					recArray['comment_count']=0

					recArray['id']=userPostInfos.id
					
					recArray['post_file_url']=userPostInfos.post_file_url
					recArray['post_title']=userPostInfos.post_title
					recArray['post_description']=''
					recArray['hash_tag']=''
					recArray['posted_on']=str(userPostInfos.posted_on)
					recArray['posted_at']=str(userPostInfos.posted_at)
					recArray['user_by_id']=userPostInfos.userid
					recArray['title']=userPostInfos.post_title
					
					postlike="SELECT id,sum(num_likes) as likes, sum(num_share) as share  FROM soapbox_postlikeandshare where post_id="+str(userPostInfos.id)+";"
					for postlikes in SoapboxPostlikeandshare.objects.raw(postlike):
				
						if(postlikes.share == None):
							recArray['share_count']=0
						else:
							recArray['share_count']=int(postlikes.share)
						if(postlikes.likes == None):
							recArray['like_count']=0
						else:
							recArray['like_count']=int(postlikes.likes)
					
					
					
					records.append(recArray)
					
					
					hashInfo=SoapboxPosts.objects.all().filter(userid=userid,post_file_url=recArray['post_file_url'])
					for hashInfos in hashInfo.all(): 
						recarray = {}
						
						recarray['hash_tag_name']=hashInfos.channel_name
						recarray['hash_tag_id']=hashInfos.channelid
						rec.append(recarray)
						recArray['hash_tag']=rec
					
			
					
				return HttpResponse(json.dumps({'success':1,'data':records}))
			else: 
				
				return HttpResponse(json.dumps({'message':'No Result Found.','success':0,'data': records}))			
		except Exception as e:
			return HttpResponse(json.dumps({'message':e,'success':0}))
			
			
			
def	headerinfo(request):
	if (request.META.get('HTTP_AUTHKEY') == None):
		return 0
	else:
		try:
			chkheader=SoapboxAppusers.objects.get(apikey=request.META.get('HTTP_AUTHKEY'))
			return 1
		except SoapboxAppusers.DoesNotExist:
			return 2	

def like(request):
	headervalue = headerinfo(request);
	
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
		try:
			like_json_data=json.loads(request.body)
			userid = like_json_data['user_id']
			post_id = like_json_data['post_id']
			if(userid == ''):
				return HttpResponse(json.dumps({'message':'userid is Missing.','success':'0'}))
			if(post_id ==''):
				return HttpResponse(json.dumps({'message':'post_id is Missing.','success':'0'}))
			
			if(userid !='' and post_id!='' ):
			
				try:
					postlike = SoapboxPostlikeandshare.objects.get(user_id=userid,post_id=post_id)
					SoapboxPostlikeandshare.objects.filter(user_id=userid,post_id=post_id).delete()
					return HttpResponse(json.dumps({"success":0,"message": "post unlike  successfully."}))
				
				except SoapboxPostlikeandshare.DoesNotExist:
					like=SoapboxPostlikeandshare(user_id=userid,post_id=post_id,num_likes=1,num_share=0)
					like.save()
					return HttpResponse(json.dumps({"success":1,"message": "like successfully."}))
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error))
		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))

def getPopularPostList(request):
	headervalue = headerinfo(request);
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
		try:
			rec =[]
			getPopularPostList_json_data=json.loads(request.body)
			userid = getPopularPostList_json_data['user_id']
			if(userid == ''):
				return HttpResponse(json.dumps({'message':'userid is Missing.','success':'0'}))
			
				# postlike=SoapboxPostlikeandshare.objects.filter(user_id=userid).values('post_id').annotate(total=Sum('num_share')).order_by('-total')
				# data = serializers.serialize('json', postlike, fields=('user_id','id'))
				# return HttpResponse(data)
				
			postlike = "SELECT id,post_id, user_id, sum( num_share ) as total ,sum( num_likes ) as likes FROM soapbox_postlikeandshare WHERE user_id ="+str(userid)+" GROUP BY post_id ORDER BY total DESC , likes DESC;"
		
			for postlikes in SoapboxPostlikeandshare.objects.raw(postlike):
				recarray = {}
				record =[]
				recarray['share_count']=int(postlikes.total)
				recarray['id']=postlikes.id
				recarray['like_count']=int(postlikes.likes)
				recarray['user_by_id']=postlikes.user_id
				
				try:
					chkpost = SoapboxPosts.objects.get(id=postlikes.post_id)
					chkusr=SoapboxAppusers.objects.get(id=userid)
					
					recarray['username']=chkusr.username
					recarray['profilepic']=chkusr.profilepic
					
					recarray['listen_count']=0

					recarray['comment_count']=0

					recarray['post_file_url']=chkpost.post_file_url
					recarray['post_description']=''
					recarray['post_title']=chkpost.post_title
					recarray['posted_at']=str(chkpost.posted_at)
					recarray['posted_on']=str(chkpost.posted_on)
					#recarray['custom_tag_id']=chkpost.channelid
					rec.append(recarray)
					hashInfo=SoapboxPosts.objects.all().filter(userid=userid,post_file_url=chkpost.post_file_url)
					for hashInfos in hashInfo.all(): 
						recArray = {}
						 
						recArray['hash_tag_name']=hashInfos.channel_name
						recArray['hash_tag_id']=hashInfos.channelid
						record.append(recArray)
						
						recarray['hash_tag']=record
						#rec.append(recArray)
						#recarray['hash_tag']=rec
				except SoapboxPosts.DoesNotExist:
					recarray['post_file_url']=''
					recarray['post_description']=''
					recarray['post_title']=''
					recarray['posted_at']=''
					recarray['posted_on']=''
					#recarray['custom_tag_id']=''
					rec.append(recarray)
			
			
			return HttpResponse(json.dumps({"success":1,"data":rec,'message':'success'}))
			
		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
	
	


	
def getUserList(request):
	headervalue = headerinfo(request);
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
		try:
			rec =[]
			
			getuserlist_json_data=json.loads(request.body)
			friend_list = getuserlist_json_data['friend_list']
			if(friend_list == ''):
				return HttpResponse(json.dumps({'message':'friend_list is Missing.','success':'0'}))
			else:
				friendInfo = SoapboxAppusers.objects.all().filter(socialid__in=friend_list)
				if friendInfo.exists():
					for friendInfos in friendInfo.all():
						recarray = {}
						recarray['user_id']=friendInfos.id
						recarray['frist_name']=friendInfos.firstname
						recarray['last_name']=friendInfos.lastname
						recarray['username']=friendInfos.username
						recarray['email']=friendInfos.email
						recarray['dob']=str(friendInfos.dateofbirth)
						recarray['gender']=friendInfos.gender
						recarray['social_id']=friendInfos.socialid
						recarray['socialsite_name']=friendInfos.usertype
						recarray['profile_pic']=friendInfos.profilepic
						recarray['intro_audio_url']=friendInfos.intro_audio_url
						rec.append(recarray)
					return HttpResponse(json.dumps({"success":1,"data":rec,'message':'success'}))
				else:
					return HttpResponse(json.dumps({'message':'No Result Found.','success':0,"data":rec}))		
		except Exception as e:
			return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		

def getFollowingPostList(request):
	headervalue = headerinfo(request);
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
		try:
			rec=[]
			getFollowingPostList_json_data=json.loads(request.body)
			user_id = getFollowingPostList_json_data['user_id']
			if(user_id == ''):
				return HttpResponse(json.dumps({'message':'user_id is Missing.','success':'0'}))
			else:
				followingpostlist = SoapboxPosts.objects.all().filter(userid__in=SoapboxUserfollowers.objects.all().filter(user_id=user_id).values('following_user_id')).order_by('posted_at', 'posted_on')
				#SoapboxUserfollowers.objects.all().filter(user_id=user_id).values('following_user_id')
				#return HttpResponse(friendInfo)
				#friendInfo = SoapboxPosts.objects.all().filter(userid__in=SoapboxUserfollowers.objects.all().filter(user_id=user_id).values('following_user_id')).values('id')
				if followingpostlist.exists():
					for followingpostlists in followingpostlist.all(): 
						recarray ={}
						record =[]
						recarray['id']=followingpostlists.id
						recarray['post_file_url']=followingpostlists.post_file_url
						recarray['post_description']=''
						recarray['post_title']=followingpostlists.post_title
						recarray['posted_at']=str(followingpostlists.posted_at)
						recarray['posted_on']=str(followingpostlists.posted_on)
						recarray['user_by_id']=followingpostlists.userid
						chkusr=SoapboxAppusers.objects.get(id=followingpostlists.userid)
						recarray['username']=chkusr.username
						recarray['profilepic']=chkusr.profilepic
						recarray['listen_count']=0
						recarray['comment_count']=0
						
						postlike="SELECT id,sum(num_likes) as likes, sum(num_share) as share  FROM soapbox_postlikeandshare where post_id="+str(followingpostlists.id)+";"
						for postlikes in SoapboxPostlikeandshare.objects.raw(postlike):
							
							if(postlikes.share == None):
								recarray['share_count']=0
							else:
								recarray['share_count']=int(postlikes.share)
							if(postlikes.likes == None):
								recarray['like_count']=0
							else:
								recarray['like_count']=int(postlikes.likes)
							
						
							rec.append(recarray)
						hashInfo=SoapboxPosts.objects.all().filter(userid=followingpostlists.userid,post_file_url=followingpostlists.post_file_url)
						for hashInfos in hashInfo.all(): 
							recArray = {}
							recArray['hash_tag_name']=hashInfos.channel_name
							recArray['hash_tag_id']=hashInfos.channelid
							record.append(recArray)
							recarray['hash_tag']=record
					#return HttpResponse(json.dumps(list(friendInfo), cls=DjangoJSONEncoder))
					return HttpResponse(json.dumps({"success":1,"data":rec,'message':'success'}))
				else :
					return HttpResponse(json.dumps({"success":0,"data":rec}))
		except Exception as e:
			return HttpResponse(json.dumps({'message':e,'success':0}))	
	
	
	
	
	
	
	
	
	
	
	
	
	
	