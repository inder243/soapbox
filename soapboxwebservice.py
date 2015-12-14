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

from soapbox.models import SoapboxAppusers ,SoapboxDevicetoken,SoapboxCategories,SoapboxConnectiontablesocialid,SoapboxSubscribechannel,SoapboxPosts

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
		devicetype =received_json_data['devicet_type']
		devicetoken = received_json_data['device_id']
		intro_audio_url = received_json_data['intro_audio_url']

			
		if(firstname == ''):
			return HttpResponse(json.dumps({'message':'Firstname is Missing.','success':0}))
		if(lastname ==''):
			return HttpResponse(json.dumps({'message':'Lastname is Missing.','success':0}))
		if(username ==''): 
			return HttpResponse(json.dumps({'message':'Username is Missing.','success':0}))
		#if(dateofbirth ==''): 
			#dateofbirth = '1111-11-11'
		if(email ==''):
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
	except Exception as e:
		return HttpResponse(json.dumps({'message':e,'success':0}))
		

	
	
	
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
			
			channelInfo=SoapboxCategories.objects.all().filter(created_by_id=userid,channel_name__icontains=channelname)
			if channelInfo.exists():
				for channeldata in channelInfo.all(): 
					arr={}
					arr['channel_name'] = channeldata.channel_name
					arr['channel_id'] = channeldata.id
					records.append(arr)
					
				return HttpResponse(json.dumps({'message':'stored channel name','channel_name':records}))
			else:
			
				# channelSave=SoapboxCategories(created_by_id=userid,channel_name=channelname,created_at=nowTime,type_of_channel=1)
				# channelSave.save()
				# user_id=channelSave.pk
				# categoryInfo={'userid':user_id,'channel':channelname}
				# return HttpResponse(json.dumps({'message':'channel add successfully.','success':1,'category':categoryInfo}))
				return HttpResponse(json.dumps({'message':'No Result Found.','success':1}))
		else:
			error={'error':'invalid parameters'}
			return HttpResponse(json.dumps(error))
	
	except Exception as e:
		return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))	
	
		
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
		
		
def subscribechannel(request):
	try:
		subscribechannel_json_data=json.loads(request.body)
		recArray={}
		userid = subscribechannel_json_data['userid']
		channel_id = subscribechannel_json_data['channelid']
		issubscribe = subscribechannel_json_data['issubscribe']
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
		rawdata = audio_json_data['rawdata']
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
			return HttpResponse(json.dumps({'audioUrl':audiourl,'success':1}))	
		elif(type == '2'):
			filename=  nowTime.strftime("%S%H%M%f")+'.'+extension
			fh = open(settings.BASE_DIR+"/soapbox/profilepic/"+filename, "wb")
			fh.write(rawdata.decode('base64'))
			fh.close()
			baseurl = request.build_absolute_uri('/')[:-6]
			imageurl= baseurl+"/soapbox/soapbox/profilepic/"+filename
			return HttpResponse(json.dumps({'imageUrl':imageurl,'success':1}))	
		else:
			return HttpResponse(json.dumps({'message':'Incorrect format type.','success':0}))	
		
			
	
	except Exception as e:
		return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		
		
def postAudioMessage(request):
	#try:
	
		nowTime = datetime.datetime.now()
		postaudio_json_data=json.loads(request.body)
		userid = postaudio_json_data['user_id']
		hashtag_name = postaudio_json_data['hashtag_name']
		hash_tag_id = postaudio_json_data['hash_tag_id']
		audiofile = postaudio_json_data['audiofile']
		#title =  postaudio_json_data['title']
		
		if(userid == ''):
			return HttpResponse(json.dumps({'message':'userid is Missing.','success':'0'}))
		if(audiofile ==''):
			return HttpResponse(json.dumps({'message':'audiofile is Missing.','success':'0'}))
		if(hash_tag_id ==''):
			return HttpResponse(json.dumps({'message':'hash_tag_id is Missing.','success':'0'}))
		if(hashtag_name == ''):
			return HttpResponse(json.dumps({'message':'hashtag_name is Missing.','success':'0'}))
		# if(title ==''):
			# return HttpResponse(json.loads({'message':'title is Missing.','success':'0'}))
		
		if(userid !='' and audiofile!='' and hash_tag_id!='' and hashtag_name!=''  ):
			#post=SoapboxPosts(userid=userid,post_file_url=audiofile,posted_on=nowTime)
			#post.save()
			posted_on=nowTime.strftime("%Y-%m-%d")
			posted_at=nowTime.strftime("%H:%M:%S")
			post=SoapboxPosts(userid=userid,post_file_url=audiofile,posted_on=nowTime,posted_at=posted_at,channelid=hash_tag_id,channel_name=hashtag_name)
			post.save()
			post_id = str(post.pk)
			data={"id":post_id,"post_file_url":audiofile,"posted_on":posted_on,"posted_at":posted_at,"user_by_id":userid,"hash_tag_id":hash_tag_id,"hash_tag_name":hashtag_name}
	  
			return HttpResponse(json.dumps({"success": 1,'message':'save successfully','data':data}))
		else:
			error={'error':'invalid parameters'}
			return HttpResponse(json.dumps(error))
	#except Exception as e:
		#return HttpResponse(json.dumps({'message':'Invalid Data.','success':0}))
		
def follow(request):
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
		
