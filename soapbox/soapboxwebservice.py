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
from soapbox.models import SoapboxAppusers ,SoapboxDevicetoken,SoapboxCategories,SoapboxPostshares,SoapboxComments,SoapboxPostlistens,SoapboxPostlikes,SoapboxTagrelatedtopost,SoapboxConnectiontablesocialid,SoapboxSubscribechannel,SoapboxPosts,SoapboxPostlikeandshare,SoapboxUserfollowers

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
		channelInformation=[]
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
				userInfo={'Subscribe_Channel':channelInformation,'intro_audio_url':intro_audio_url,'site_name':'appuser','apikey':apikey,'user_id':user_id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
				return HttpResponse(json.dumps({'message':'Registered successfully with Soapbox App.','success':1,'information':userInfo}))
			else:
				userInfo={'Subscribe_Channel':channelInformation,'intro_audio_url':intro_audio_url,'site_name':'appuser','apikey':apikey,'user_id':user_id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
				return HttpResponse(json.dumps({'message':'Registered successfully with Soapbox App.','success':1,'information':userInfo}))
		
		
		elif (socialid != '' and usertype != 0):
			
			try:
				chkuserinfo=SoapboxAppusers.objects.get(socialid=socialid)
				
				updateValue ={"intro_audio_url":intro_audio_url,"firstname": firstname,"lastname": lastname,"username":username,"email":email,"dateofbirth":dateofbirth,"gender":gender,"profilepic":imageurl}
				userSave=SoapboxAppusers.objects.filter(socialid=socialid).update(**updateValue)
				channelInfo=SoapboxSubscribechannel.objects.all().filter(userid=chkuserinfo.id,issubscribe=1)
				
				if channelInfo.exists():
					for channeldata in channelInfo.all(): 
						channelInfoArray={}
						#arr['channel_name'] = channeldata.channel_name
						channelInfoArray['channel_id'] = channeldata.channelid
						channelInfoArray['channel_name'] = SoapboxCategories.objects.get(id=channelInfoArray['channel_id']).channel_name
						
						channelInformation.append(channelInfoArray)
						#recArray['Subscribe_Channel']=channelInformation	
				else:
					channelInformation=[]
				if(devicetoken!='' and devicetype!=''):
					updateValue ={"devicetoken":devicetoken,"devicetype": devicetype}
					SoapboxDevicetoken.objects.filter(userid=chkuserinfo.id).update(**updateValue)
					
					userInfo={'Subscribe_Channel':channelInformation,'intro_audio_url':chkuserinfo.intro_audio_url,'socialsite_name':chkuserinfo.usertype,'apikey':chkuserinfo.apikey,'social_id':socialid,'user_id':chkuserinfo.id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
					return HttpResponse(json.dumps({'message':'Login successfully with Soapbox App.','success':1,'information':userInfo}))
				else:
					userInfo={'Subscribe_Channel':channelInformation,"intro_audio_url":intro_audio_url,'socialsite_name':chkuserinfo.usertype,'apikey':chkuserinfo.apikey,'social_id':socialid,'user_id':chkuserinfo.id,'first_name':firstname,'last_name':lastname,'username':username,'email':email,'dob':dateofbirth,'gender':gender,'profile_pic':imageurl}
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
				recArray['Subscribe_Channel']=''
				#recArray['phonenumber']=userInfo.phonenumber
				recArray['intro_audio_url']=userInfo.intro_audio_url
				channelInfo=SoapboxSubscribechannel.objects.all().filter(userid=userInfo.id,issubscribe=1)
				channelInformation=[]
				if channelInfo.exists():
					for channeldata in channelInfo.all(): 
						channelInfoArray={}
						#arr['channel_name'] = channeldata.channel_name
						channelInfoArray['channel_id'] = channeldata.channelid
						channelInfoArray['channel_name'] = SoapboxCategories.objects.get(id=channelInfoArray['channel_id']).channel_name
						
						channelInformation.append(channelInfoArray)
						recArray['Subscribe_Channel']=channelInformation	
				else:
					recArray['Subscribe_Channel']=channelInformation
				
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
		return HttpResponse(json.dumps({'message':e,'success':0}))
		
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
						return HttpResponse(json.dumps({'success':1,'message':'Channel Unsubscribed successfully'}))
					
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
				
			returnpostid=SoapboxTagrelatedtopost(user_id=userid,post_file_url=audiofile,post_title=title,posted_on=nowTime,posted_at=posted_at)
			returnpostid.save()
			retpostid=str(returnpostid.pk)

			post_json_data=json.loads(request.body)
			jsonData = post_json_data["hashtags"]
			for item in jsonData:
					
				channelinfos = SoapboxCategories.objects.all().filter(channel_name= item.get("hash_tag_name"),id =item.get("id"))
				
				if channelinfos.exists():
				
					
					post=SoapboxPosts(userid=userid,post_id=retpostid,matter_msg_id=0,channelid=item.get("id"),channel_name=item.get("hash_tag_name"))
					post.save()
					post_id = str(post.pk)
					recArray={"id":retpostid,"post_title":title,"post_file_url":audiofile,"posted_on":posted_on,"posted_at":posted_at,"user_by_id":userid,"hash_tag_id":item.get("id"),"hash_tag_name":item.get("hash_tag_name")}
					records.append(recArray)
					
				else:
					
					channelSave=SoapboxCategories(created_by_id=userid,channel_name=item.get("hash_tag_name"),created_at=nowTime,type_of_channel=1)
					channelSave.save()
					channel_id=channelSave.pk
				
					post=SoapboxPosts(userid=userid,post_id=retpostid,matter_msg_id=0,channelid=channel_id,channel_name=item.get("hash_tag_name"))
					post.save()
					post_id = str(post.pk)
					recArray={"id":retpostid,"post_title":title,"post_file_url":audiofile,"posted_on":posted_on,"posted_at":posted_at,"user_by_id":userid,"hash_tag_id":channel_id,"hash_tag_name":item.get("hash_tag_name")}
					records.append(recArray)
			return HttpResponse(json.dumps({"success": 1,'message':'save successfully','data':records}))
			

		except Exception as e:
			return HttpResponse(json.dumps({'message':e,'success':0}))
		
		
		
		
		
		
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
					return HttpResponse(json.dumps({"success":1,"message": "user unfollow successfully."}))
				
				except SoapboxUserfollowers.DoesNotExist:
					follow=SoapboxUserfollowers(following_user_id=following_user_id,user_id=userid)
					follow.save()
					return HttpResponse(json.dumps({"success":1,"message": "followed successfully."}))
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error))
		except Exception as e:
			return HttpResponse(json.dumps({'message':e,'success':0}))
	
	
	
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
				
				returnpostid=SoapboxTagrelatedtopost(user_id=userid,post_file_url=audiofile,post_title='',posted_on=nowTime,posted_at=posted_at)
				returnpostid.save()
				retpostid=str(returnpostid.pk)
				post=SoapboxPosts(userid=userid,post_id=retpostid,matter_msg_id=matter_msg_id,channelid=0,channel_name="")
				post.save()
				
				comment= SoapboxComments(user_id=userid,comment=audiofile,comment_on=posted_on,comment_at=posted_at,post_id=matter_msg_id)
				comment.save()
				
				try:
					pcomment = SoapboxPostlikeandshare.objects.get(user_id=userid,post_id=matter_msg_id)
					tcomment= pcomment.num_comment
					totalcomment = tcomment+1
					pcomment.num_comment = totalcomment
					pcomment.save()
					#return HttpResponse(json.dumps({"success":1,"message": "comment successfully."}))
				except SoapboxPostlikeandshare.DoesNotExist:
					pcomment=SoapboxPostlikeandshare(user_id=userid,post_id=matter_msg_id,num_likes=0,num_share=0,num_listen=0,num_comment=1)
					pcomment.save()
				
				
				post_id = str(post.pk)
				data={"user_by_id": userid,"post_file_url":audiofile,"posted_on":posted_on,"posted_at":posted_at,"id":retpostid}
				
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

            userPostInfo=SoapboxTagrelatedtopost.objects.all().filter(user_id=userid).order_by('-id')
            chkusr=SoapboxAppusers.objects.get(id=userid)
            userrec ={}
            recArray = {}
            postAllArrayData=[]


            if userPostInfo.exists():
                for userPostInfos in userPostInfo.all():

                    postArray={}

                    postlike="SELECT id,sum(num_likes) as likes, sum(num_share) as share, sum(num_listen) as listen ,count(num_comment)as total_comment FROM soapbox_postlikeandshare where post_id="+str(userPostInfos.id)+";"
                    for postlikes in SoapboxPostlikeandshare.objects.raw(postlike):

                        if(postlikes.share == None):
                            postArray['share_count']=0
                        else:
                            postArray['share_count']=int(postlikes.share)
                        if(postlikes.likes == None):
                            postArray['like_count']=0
                        else:
                            postArray['like_count']=int(postlikes.likes)
                        if(postlikes.listen == None):
                            postArray['listen_count']=0
                        else:
                            postArray['listen_count']=int(postlikes.listen)

                    postArray['username']=chkusr.username
                    postArray['profilepic']=chkusr.profilepic
                    postArray['comment_count']=int(postlikes.total_comment)
                    postArray['id']=userPostInfos.id
                    postArray['post_file_url']=userPostInfos.post_file_url
                    postArray['post_title']=userPostInfos.post_title
                    postArray['post_description']=''
                    postArray['hash_tag']=''
                    postArray['posted_on']=str(userPostInfos.posted_on)
                    postArray['posted_at']=str(userPostInfos.posted_at)
                    postArray['user_by_id']=userPostInfos.user_id
                    try:
                        postlikeornot=SoapboxPostlikes.objects.get(user_id=userid,post_id=userPostInfos.id)
                        postArray['is_like']="true"
                    except SoapboxPostlikes.DoesNotExist:
                        postArray['is_like']="false"

                    #fetching hash tags
                    hashInfo=SoapboxPosts.objects.all().filter(post_id=userPostInfos.id)
                    hashTagSingArray=[]
                    for hashInfos in hashInfo.all(): 
                        hashTagArray = {}

                        hashTagArray['hash_tag_name']=hashInfos.channel_name
                        hashTagArray['hash_tag_id']=hashInfos.channelid
                        hashTagSingArray.append(hashTagArray)
                    postArray['hash_tag']=hashTagSingArray	
                    postAllArrayData.append(postArray)


                return HttpResponse(json.dumps({'success':1,'data':postAllArrayData}))

            else: 

                return HttpResponse(json.dumps({'message':'No Result Found.','success':1,'data': records}))			
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
            postAllArrayData =[]
            getPopularPostList_json_data=json.loads(request.body)
            userid = getPopularPostList_json_data['user_id']
            if(userid == ''):
                return HttpResponse(json.dumps({'message':'userid is Missing.','success':'0'}))
            else:
                postlike = "SELECT * , count( num_share ) AS total_share, count( num_likes ) AS total_likes, count( num_comment ) AS total_comment, count( num_listen ) AS listen_count,soapbox_tagrelatedtopost.id as postid,soapbox_tagrelatedtopost.user_id as userid FROM soapbox_posts LEFT JOIN soapbox_tagrelatedtopost ON soapbox_posts.post_id = soapbox_tagrelatedtopost.id LEFT JOIN soapbox_postlikeandshare ON soapbox_postlikeandshare.post_id = soapbox_tagrelatedtopost.id WHERE soapbox_posts.channelid IN (SELECT channelid FROM soapbox_subscribechannel WHERE userid ="+str(userid)+") OR soapbox_tagrelatedtopost.user_id ="+str(userid)+" GROUP BY soapbox_tagrelatedtopost.id ORDER BY total_share DESC , listen_count DESC , total_likes DESC"
                #postlike = "SELECT * , count( num_share ) AS total_share, count( num_likes ) AS total_likes, count( num_comment ) AS total_comment, count( num_listen ) AS listen_count,soapbox_tagrelatedtopost.id as postid,soapbox_tagrelatedtopost.user_id as userid FROM soapbox_posts LEFT JOIN soapbox_tagrelatedtopost ON soapbox_posts.post_id = soapbox_tagrelatedtopost.id LEFT JOIN soapbox_postlikeandshare ON soapbox_postlikeandshare.post_id = soapbox_tagrelatedtopost.id WHERE soapbox_posts.channelid IN (SELECT channelid FROM soapbox_subscribechannel WHERE userid =66 ) OR soapbox_tagrelatedtopost.user_id =66 GROUP BY soapbox_tagrelatedtopost.id ORDER BY total_share DESC , listen_count DESC , total_likes DESC"
            	#postlike = "select *,count(num_share)as total_share,count(num_likes)as total_likes,count(num_comment)as total_comment,count(num_listen)as listen_count ,soapbox_tagrelatedtopost.id as postid,soapbox_tagrelatedtopost.user_id as userid   from  soapbox_tagrelatedtopost left join  soapbox_postlikeandshare on  soapbox_postlikeandshare.post_id=soapbox_tagrelatedtopost.id  where  soapbox_tagrelatedtopost.user_id ="+str(userid)+" group by soapbox_tagrelatedtopost.id order by total_share DESC ,listen_count DESC, total_likes DESC"
                if not SoapboxSubscribechannel.objects.filter(userid=userid):
                    
                    return HttpResponse(json.dumps({'success':1,'data':postAllArrayData,'message':'no data found'}))
                else:
                    for postlikes in SoapboxTagrelatedtopost.objects.raw(postlike):
                        postArray ={}
              
                        chkusr=SoapboxAppusers.objects.get(id=userid)	
                        postArray['username']=chkusr.username
                        postArray['profilepic']=chkusr.profilepic
                        
                        if(postlikes.total_comment == None):
                            postArray['comment_count']=0
                        else:
                            postArray['comment_count']=int(postlikes.total_comment)
                        
                        if(postlikes.total_share == None):
                            postArray['share_count']=0
                        else:
                            postArray['share_count']=int(postlikes.total_share)
                        if(postlikes.total_likes == None):
                            postArray['like_count']=0
                        else:
                            postArray['like_count']=int(postlikes.total_likes)
                        if(postlikes.listen_count == None):
                            postArray['listen_count']=0
                        else:
                            postArray['listen_count']=int(postlikes.listen_count)
                            
                        
                        # userPostInfo=SoapboxTagrelatedtopost.objects.all().filter(id=postlikes.postid,user_id=postlikes.userid)
                        # for userPostInfos in userPostInfo.all():
                        postArray['id']=postlikes.id
                        postArray['post_file_url']=postlikes.post_file_url
                        postArray['post_title']=postlikes.post_title
                        postArray['post_description']=''
                        postArray['hash_tag']=''
                        postArray['posted_on']=str(postlikes.posted_on)
                        postArray['posted_at']=str(postlikes.posted_at)
                        postArray['user_by_id']=postlikes.user_id
                                
                           
                       
                        try:
                            postlikeornot=SoapboxPostlikes.objects.get(user_id=userid,post_id=postlikes.postid)
                            postArray['is_like']="true"
                        except SoapboxPostlikes.DoesNotExist:
                            postArray['is_like']="false"
                             # #fetching hash tags
                        hashInfo=SoapboxPosts.objects.all().filter(post_id=postlikes.postid)
                        hashTagSingArray=[]
                        for hashInfos in hashInfo.all(): 
                            hashTagArray = {}
                            
                            hashTagArray['hash_tag_name']=hashInfos.channel_name
                            hashTagArray['hash_tag_id']=hashInfos.channelid
                            hashTagSingArray.append(hashTagArray)
                        postArray['hash_tag']=hashTagSingArray	
                        postAllArrayData.append(postArray)
                            
                    return HttpResponse(json.dumps({'success':1,'data':postAllArrayData}))
        except Exception as e:
            return HttpResponse(json.dumps({'message':e,'success':0}))
	


	
def getUserList(request):
	headervalue = headerinfo(request);
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
		try:
			recFriend =[]
			
			getuserlist_json_data=json.loads(request.body)
			friend_list = getuserlist_json_data['friend_list']
			if(friend_list == ''):
				return HttpResponse(json.dumps({'message':'friend_list is Missing.','success':'0'}))
			else:
				friendInfo = SoapboxAppusers.objects.all().filter(socialid__in=friend_list)
				if friendInfo.exists():
					for friendInfos in friendInfo.all():
						recFriendArray = {}
						rerecFriendArraycarray['user_id']=friendInfos.id
						recFriendArray['frist_name']=friendInfos.firstname
						recFriendArray['last_name']=friendInfos.lastname
						recFriendArray['username']=friendInfos.username
						recFriendArray['email']=friendInfos.email
						recFriendArray['dob']=str(friendInfos.dateofbirth)
						recFriendArray['gender']=friendInfos.gender
						recFriendArray['social_id']=friendInfos.socialid
						recFriendArray['socialsite_name']=friendInfos.usertype
						recFriendArray['profile_pic']=friendInfos.profilepic
						recFriendArray['intro_audio_url']=friendInfos.intro_audio_url
						recFriend.append(recFriendArray)
					return HttpResponse(json.dumps({"success":1,"data":recFriend,'message':'success'}))
				else:
					return HttpResponse(json.dumps({'message':'No Result Found.','success':1,"data":recFriend}))		
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
            postAllArrayData=[]
            getFollowingPostList_json_data=json.loads(request.body)
            user_id = getFollowingPostList_json_data['user_id']
            if(user_id == ''):
                return HttpResponse(json.dumps({'message':'user_id is Missing.','success':'0'}))
            else:
                followingpostlist = SoapboxTagrelatedtopost.objects.all().filter(user_id__in=SoapboxUserfollowers.objects.all().filter(user_id=user_id).values('following_user_id')).order_by('posted_at', 'posted_on')
                if followingpostlist.exists():
                    for followingpostlists in followingpostlist.all(): 
                        postArray ={}
                        postArray['id']=followingpostlists.id
                        chkusr=SoapboxAppusers.objects.get(id=postArray['id'])	
                        postArray['username']=chkusr.username
                        postArray['profilepic']=chkusr.profilepic
                        postArray['post_file_url']=followingpostlists.post_file_url
                        postArray['post_title']=followingpostlists.post_title
                        postArray['post_description']=''
                        postArray['hash_tag']=''
                        postArray['posted_on']=str(followingpostlists.posted_on)
                        postArray['posted_at']=str(followingpostlists.posted_at)
                        postArray['user_by_id']=followingpostlists.user_id
                        try:
                            postlikeornot=SoapboxPostlikes.objects.get(user_id=user_id,post_id=followingpostlists.id)
                            postArray['is_like']="true"
                        except SoapboxPostlikes.DoesNotExist:
                            postArray['is_like']="false"
                        # #fetching hash tags
                        hashInfo=SoapboxPosts.objects.all().filter(post_id=followingpostlists.id)
                        hashTagSingArray=[]
                        for hashInfos in hashInfo.all(): 
                            hashTagArray = {}

                            hashTagArray['hash_tag_name']=hashInfos.channel_name
                            hashTagArray['hash_tag_id']=hashInfos.channelid
                            hashTagSingArray.append(hashTagArray)
                        postArray['hash_tag']=hashTagSingArray	


                        postlike="SELECT id,sum(num_likes) as likes, sum(num_listen) as listen, sum(num_share) as share,count(num_comment)as total_comment  FROM soapbox_postlikeandshare where post_id="+str(followingpostlists.id)+";"
                        for postlikes in SoapboxPostlikeandshare.objects.raw(postlike):

                            if(postlikes.share == None):
                                postArray['share_count']=0
                            else:
                                postArray['share_count']=int(postlikes.share)
                            if(postlikes.likes == None):
                                postArray['like_count']=0
                            else:
                                postArray['like_count']=int(postlikes.likes)
                            if(postlikes.listen == None):
                                postArray['like_listen']=0
                            else:
                                postArray['like_listen']=int(postlikes.listen)

                            if(postlikes.total_comment == None):
                                postArray['comment_count']=0
                            else:
                                postArray['comment_count']=int(postlikes.total_comment)


                            postAllArrayData.append(postArray)

                    return HttpResponse(json.dumps({"success":1,"data":postAllArrayData,'message':'success'}))
                else :
                    return HttpResponse(json.dumps({"success":1,"data":postAllArrayData,'message':'data not found'}))
        except Exception as e:
            return HttpResponse(json.dumps({'message':e,'success':0}))
			
def postReplyOther(request):
	headervalue = headerinfo(request);
	
	if(headervalue == 0):
		return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
	elif(headervalue == 2) :
		return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
	else:
		try:
			like_json_data=json.loads(request.body)
			userid = like_json_data['user_id']
			post_id = like_json_data['master_msg_id']
			other_reply_type = like_json_data['other_reply_type']
			
			nowTime = datetime.datetime.now()
			posted_on=nowTime.strftime("%Y-%m-%d")
			posted_at=nowTime.strftime("%H:%M:%S")
			
			if(userid == ''):
				return HttpResponse(json.dumps({'message':'userid is Missing.','success':0}))
			if(post_id ==''):
				return HttpResponse(json.dumps({'message':'post_id is Missing.','success':0}))
			if(other_reply_type ==''):
				return HttpResponse(json.dumps({'message':'other_reply_type is Missing.','success':0}))
			if(userid !='' and post_id!=''and other_reply_type!='' ):
				if(other_reply_type == 1):
					# like= SoapboxPostlikes(user_id=userid,post_id=post_id,like_on=posted_on,like_at=posted_at,num_likes=1)
					# like.save()
					try:
						like = SoapboxPostlikeandshare.objects.get(user_id=userid,post_id=post_id)
						tlike= like.num_likes
						tlike = 1
						like.num_likes = tlike
						like.save()
						
						try:
							likes = SoapboxPostlikes.objects.get(user_id=userid,post_id=post_id)
							totallike= likes.num_likes
							totallike = 1
							likes.num_likes = totallike
							likes.save()
							#return HttpResponse(json.dumps({"success":1,"message": "like successfully."}))
						except SoapboxPostlikes.DoesNotExist:
						
							like= SoapboxPostlikes(user_id=userid,post_id=post_id,like_on=posted_on,like_at=posted_at,num_likes=1)
							like.save()
						return HttpResponse(json.dumps({"success":1,"message": "like successfully."}))
						
					except SoapboxPostlikeandshare.DoesNotExist:
						like=SoapboxPostlikeandshare(user_id=userid,post_id=post_id,num_likes=1,num_share=0,num_listen=0,num_comment=0)
						like.save()
						like= SoapboxPostlikes(user_id=userid,post_id=post_id,like_on=posted_on,like_at=posted_at,num_likes=1)
						like.save()
						return HttpResponse(json.dumps({"success":1,"message": "like successfully."}))
					
				elif(other_reply_type == 2):
					share= SoapboxPostshares(user_id=userid,post_id=post_id,share_on=posted_on,share_at=posted_at,num_shares =1)
					share.save()
					try:
						pshare = SoapboxPostlikeandshare.objects.get(user_id=userid,post_id=post_id)
						tshare= pshare.num_share
						totalshare = tshare+1
						pshare.num_share = totalshare
						pshare.save()
						return HttpResponse(json.dumps({"success":1,"message": "share successfully."}))
					except SoapboxPostlikeandshare.DoesNotExist:
						share=SoapboxPostlikeandshare(user_id=userid,post_id=post_id,num_likes=0,num_share=1,num_listen=0,num_comment=0)
						share.save()
						return HttpResponse(json.dumps({"success":1,"message": "share successfully."}))
				elif(other_reply_type == 3):
					
					listen= SoapboxPostlistens(user_id=userid,post_id=post_id,listen_on=posted_on,listen_at=posted_at,num_listens=1)
					listen.save()
					try:
						plisten= SoapboxPostlikeandshare.objects.get(user_id=userid,post_id=post_id)
						tlisten= plisten.num_listen
						totallisten = tlisten+1
						plisten.num_listen = totallisten
						plisten.save()
						return HttpResponse(json.dumps({"success":1,"message": "listen successfully."}))
					except SoapboxPostlikeandshare.DoesNotExist:	
						listen=SoapboxPostlikeandshare(user_id=userid,post_id=post_id,num_likes=0,num_share=0,num_listen=1,num_comment=0)
						listen.save()
						return HttpResponse(json.dumps({"success":1,"message": "listen successfully."}))
				
				elif(other_reply_type == 4):
					updateValue={"num_likes":0}
					userSave=SoapboxPostlikeandshare.objects.filter(post_id=post_id,user_id=userid).update(**updateValue)
					SoapboxPostlikes.objects.filter(post_id=post_id,user_id=userid).update(**updateValue)
					return HttpResponse(json.dumps({"success":1,"message": "post unlike  successfully."}))
				else:
					return HttpResponse(json.dumps({"success":1,"message": "Other_reply_type is incorrect."}))
					
			else:
				error={'error':'invalid parameters'}
				return HttpResponse(json.dumps(error))
		except Exception as e:
			return HttpResponse(json.dumps({'message':e,'success':0}))	
	
	
def getUserProfile(request):
    headervalue = headerinfo(request);
    if(headervalue == 0):
        return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
    elif(headervalue == 2) :
        return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
    else:
        try:
            recUserProfile =[]
            getuserprofile_json_data=json.loads(request.body)
            userid = getuserprofile_json_data['user_id']
            if(userid == ''):
                return HttpResponse(json.dumps({'message':'user_id is Missing.','success':'0'}))
            else:
                userProfileInfo = SoapboxAppusers.objects.get(id=userid)
                recprofileArray = {}
                recprofileArray['user_id']=userProfileInfo.id
                recprofileArray['frist_name']=userProfileInfo.apikey
                recprofileArray['frist_name']=userProfileInfo.firstname
                recprofileArray['last_name']=userProfileInfo.lastname
                recprofileArray['username']=userProfileInfo.username
                recprofileArray['email']=userProfileInfo.email
                recprofileArray['dob']=str(userProfileInfo.dateofbirth)
                recprofileArray['gender']=userProfileInfo.gender
                recprofileArray['social_id']=userProfileInfo.socialid
                recprofileArray['socialsite_name']=userProfileInfo.usertype
                recprofileArray['profile_pic']=userProfileInfo.profilepic
                recprofileArray['intro_audio_url']=userProfileInfo.intro_audio_url
                recUserProfile.append(recprofileArray)
                return HttpResponse(json.dumps({"success":1,"data":recUserProfile,'message':'success'}))
       	
        except Exception as e:
            return HttpResponse(json.dumps({'message':e,'success':0}))	

            
            
def editProfile(request):
    headervalue = headerinfo(request);
    if(headervalue == 0):
        return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
    elif(headervalue == 2) :
        return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
    else:
        try:
            editProfile_json_data=json.loads(request.body)
            userid = editProfile_json_data['user_id']
            firstname= editProfile_json_data['first_name']
            lastname=editProfile_json_data['last_name']
            username=editProfile_json_data['username']
            dateofbirth=editProfile_json_data['dob']
            gender=editProfile_json_data['gender']
            profileimage=editProfile_json_data['profile_pic']
            intro_audio_url = editProfile_json_data['intro_audio_url']
            if(userid == ''):
                return HttpResponse(json.dumps({'message':'user_id is Missing.','success':'0'}))
            else:
                updateValue ={"intro_audio_url":intro_audio_url,"firstname": firstname,"lastname": lastname,"username":username,"dateofbirth":dateofbirth,"gender":gender,"profilepic":profileimage}
                userSave=SoapboxAppusers.objects.filter(id=userid).update(**updateValue)	
                return HttpResponse(json.dumps({"success": 1,'message':'edit successfully'}))					
        except Exception as e:
            return HttpResponse(json.dumps({'message':e,'success':0}))	
	

    
    
def getCommentPostList(request):
    headervalue = headerinfo(request);
    if(headervalue == 0):
        return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
    elif(headervalue == 2) :
        return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
    else:
        try:
            CommentPostList =[]

            getPostLikeShare_json_data=json.loads(request.body)
            postid = getPostLikeShare_json_data['post_id']
            userid  = getPostLikeShare_json_data['user_id']
            if(postid == ''):
                return HttpResponse(json.dumps({'message':'post_id is Missing.','success':'0'}))
            if(userid == ''):
                return HttpResponse(json.dumps({'message':'user_id is Missing.','success':'0'}))   
            if(postid != '' and userid != ''):

                commentpostlist="SELECT * FROM `soapbox_tagrelatedtopost` left join soapbox_posts on soapbox_tagrelatedtopost.id=soapbox_posts.post_id left join soapbox_appusers on soapbox_tagrelatedtopost.user_id= soapbox_appusers.id where soapbox_tagrelatedtopost.id ="+str(postid)+" and soapbox_tagrelatedtopost.user_id ="+str(userid)+""                        
                #if commentpostlist.exists():
                for commentpostlists in SoapboxTagrelatedtopost.objects.raw(commentpostlist):
                    commentpost = {}
                    commentpost['post_file_url']=commentpostlists.post_file_url
                    commentpost['posted_on ']=str(commentpostlists.posted_on) 
                    commentpost['posted_at']=str(commentpostlists.posted_at)
                    commentpost['username']=commentpostlists.username
                    commentpost['profilepic']=commentpostlists.profilepic
                    commentpost['user_by_id']=userid
                    commentpost['channel_name']=commentpostlists.channel_name 
                    commentpost['post_id']=commentpostlists.post_id
          
                    commentlikeinfo = "SELECT *,sum( num_likes ) AS total_likes, sum( num_share ) AS total_share, sum( num_listen ) AS total_listen, sum( num_comment ) AS total_comment FROM `soapbox_postlikeandshare` WHERE post_id ="+str(postid)+" and user_id = "+str(userid)+" ";
                    if not SoapboxPostlikeandshare.objects.filter(post_id=postid,user_id=userid):
                        commentpost['likes']=0
                        commentpost['listen_count']=0
                        commentpost['share_count']=0
                        CommentPostList.append(commentpost)
                        return HttpResponse(json.dumps({'success':1,'data':CommentPostList,'message':'success'}))
                    else:
                        for commentlikeinfos in SoapboxPostlikeandshare.objects.raw(commentlikeinfo):
                            commentpost['likes']=int(commentlikeinfos.total_likes)
                            commentpost['listen_count']=int(commentlikeinfos.total_listen)
                            commentpost['share_count']=int(commentlikeinfos.total_share)
                            CommentPostList.append(commentpost)
            return HttpResponse(json.dumps({"success":1,"data":CommentPostList,'message':'success'}))
                #else:
                    #return HttpResponse(json.dumps({'message':'No Result Found.','success':1,"data":CommentPostList}))		
        except Exception as e:
            return HttpResponse(json.dumps({'message':e,'success':0}))		
	
	
	
	
def getActivityList(request):
    headervalue = headerinfo(request);
    if(headervalue == 0):
        return HttpResponse(json.dumps({'message':'auth key information is missing.','success':0}))
    elif(headervalue == 2) :
        return HttpResponse(json.dumps({'message':'auth key information is incorrect.','success':0}))
    else:
        try:
            you=[]
            following=[]
            activitylist_json_data=json.loads(request.body)
            user_id  = activitylist_json_data['user_id']
            if(user_id == ''):
                return HttpResponse(json.dumps({'message':'user_id is Missing.','success':'0'}))   
           
            followactiveinfo=SoapboxAppusers.objects.all().filter(id__in=SoapboxUserfollowers.objects.all().filter(user_id=user_id).values('following_user_id'))
            for followactiveinfos in followactiveinfo:
                followinfo={}
                followinfo['message']=followactiveinfos.username +" started following you"
                followinfo['respective_id ']=followactiveinfos.id
                followinfo['respective_type']='user'
                followinfo['username']=followactiveinfos.username      
                followinfo['profilepic']=followactiveinfos.profilepic
            you.append(followinfo)
            followpostlistinfo="select soapbox_postlikes.id, soapbox_postlikes.post_id,soapbox_appusers.username,soapbox_appusers.profilepic,soapbox_postlikes.user_id from soapbox_postlikes left join soapbox_appusers on soapbox_postlikes.user_id = soapbox_appusers.id where soapbox_postlikes.post_id in( select id from soapbox_tagrelatedtopost where user_id="+str(user_id)+")";
            for followpostlistinfos in SoapboxPostlikes.objects.raw(followpostlistinfo):
                postlistinfo = {}
                postlistinfo['username']=followpostlistinfos.username
                postlistinfo['user_profile_url ']=followpostlistinfos.profilepic
                postlistinfo['message']=followpostlistinfos.username + " Liked your Post" 
                postlistinfo['respective_id']=followpostlistinfos.post_id
                postlistinfo['respective_type']="post"
            you.append(postlistinfo)   
            
            
            
            followuserinfo=SoapboxAppusers.objects.all().filter(id__in=SoapboxUserfollowers.objects.all().filter(following_user_id=user_id).values('user_id'))
            for followuserinfos in followuserinfo:
                followinformation={}
                followinformation['message']=followuserinfos.username +" started following " +SoapboxAppusers.objects.get(id=user_id).username
                followinformation['respective_id ']=followuserinfos.id
                followinformation['respective_type']='user'
                followinformation['username']=followuserinfos.username      
                followinformation['profilepic']=followuserinfos.profilepic
            following.append(followinformation)
            #"SELECT soapbox_tagrelatedtopost.id,soapbox_appusers.username,soapbox_appusers.profilepic,soapbox_tagrelatedtopost.user_id FROM soapbox_tagrelatedtopost LEFT JOIN soapbox_appusers ON soapbox_tagrelatedtopost.user_id = soapbox_appusers.id WHERE soapbox_tagrelatedtopost.id IN (SELECT post_id FROM `soapbox_postlikes`WHERE user_id ="+str(user_id)+")";
            followpostlist="SELECT soapbox_tagrelatedtopost.id,soapbox_appusers.username,soapbox_appusers.profilepic,soapbox_tagrelatedtopost.user_id FROM soapbox_tagrelatedtopost LEFT JOIN soapbox_appusers ON soapbox_tagrelatedtopost.user_id = soapbox_appusers.id WHERE soapbox_tagrelatedtopost.id IN (SELECT post_id FROM `soapbox_postlikes`WHERE user_id ="+str(user_id)+")";

            for followpostlists in SoapboxPostlikes.objects.raw(followpostlist):
                postlistinfos = {}
                postlistinfos['username']=followpostlists.username
                postlistinfos['user_profile_url ']=followpostlists.profilepic
                postlistinfos['message']=followpostlists.username + " Liked your Post" 
                postlistinfos['respective_id']=followpostlists.post_id
                postlistinfos['respective_type']="post"
            following.append(postlistinfos)  
         
            newarray ={'you':you,'following':following}
            return HttpResponse(json.dumps({"success":1,"data":newarray,'message':'success'}))
        except Exception as e:
            return HttpResponse(json.dumps({'message':e,'success':0}))		
