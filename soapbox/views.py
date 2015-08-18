from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import transaction
from array import array
from datetime import date
from django.conf import settings
from soapbox.models import Users, PersonalDetails, UserStatus, UserImage, UserStatus, UserFollowers, Categories, GroupUsersCategory, Posts, PostCategories, PostLikes, PostListens, PostShares, Comments, PodcastTimer
from django.core import serializers #for serialization to and from JSON, XML
import md5, json, os, MySQLdb, os, subprocess
from .form import PostForm


# Create your views here.

def index(request):
	#Home Page | Index Page
	#Code for the landing page goes here
	return HttpResponse("Soapbox under Construction")



def register(request):
	 form=PostForm();
	 return render(request, 'register.html', {'form': form})

	#rendering the registration page
	#HTML in soapbox/templates/
	#t = get_template('register.html')
	#html = t.render(Context({}))
	#return HttpResponse(html)

@csrf_exempt
def mobwebregemail(request):
	#Web Service for regisration from App - Register with Email
	try:
		username=request.POST['username']
		#Checking if a Username already exists
		chkUsr = Users.objects.get(username=username)
		records = [] #list
		recArr = {} #Array
		recArr['status']=0
		recArr['error']='Username Exists'
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)
	except Users.DoesNotExist:
		#Register the user with new username
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		passwd=request.POST['password']
		dob = str(request.POST['dob'])
		doby = dob.split("-")
		yr = int(doby[0])
		cyr = date.today().year
		age = cyr-yr
		state=request.POST['state']
		city=request.POST['city']
		email=request.POST['email']
		password = md5.new(passwd).hexdigest()
		#age=request.POST['age']
		usr = Users(username=username, email=email, password=password, status=1, user_type='user', registered_thru='email')
		usr.save()
		user_id = str(usr.pk)
		personal = PersonalDetails(user=usr, first_name=first_name, last_name=last_name, dob=dob, age=age, state=state, city=city)
		personal.save()
		records = []
		recArr = {}
		recArr['status']=1
		recArr['id']=user_id
		recArr['email']=email
		recArr['first_name']=first_name
		recArr['thru']='email'
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)
	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

@csrf_exempt
def mobwebregsocial(request):
	#Web Service for regisration from App - Register through Social Media
	try:
		username=request.POST['username']
		#Checking if a Username already exists
		chkUsr = Users.objects.get(username=username)
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']='Username Exists'
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)
	except Users.DoesNotExist:
		#Register the user with new username
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		email=request.POST['email']
		thru=request.POST['thru']
		dob=request.POST['dob']
		usr = Users(username=username, email=email, status=1, user_type='user', registered_thru=thru)
		usr.save()
		user_id = str(usr.pk)
		personal = PersonalDetails(user=usr, first_name=first_name, last_name=last_name, dob=dob, age=age, state=state, city=city)
		personal.save()
		records = []
		recArr = {}
		recArr['status']=1
		recArr['id']=user_id
		recArr['email']=email
		recArr['first_name']=first_name
		recArr['thru']=thru
		records.append0(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)
	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def addcategories(request):
	#rendering the add category page
	#HTML in soapbox/templates/
	t = get_template('addcategory.html')
	html = t.render(Context({}))
	return HttpResponse(html)

@csrf_exempt
def addcat(request):
	#Web Service To add static categories, by admin, common for all users - from app
	try:
		user_id = str(request.POST['userid'])
		category_name = request.POST['categoryname']
		usr = Users.objects.get(pk=user_id)
		category = Categories(category_name=category_name, type_of_category='static', created_by=usr)
		category.save()
		category_id=str(category.pk)
		t = get_template('addcat.html')
		html = t.render(Context({'id': category_id}))
		return HttpResponse(html)
	except Exception as e:
		#print '%s (%s)' % (e.message, type(e))
		return HttpResponse(e.message)

@csrf_exempt
def webaddcat(request):
	#Web Service To add custom Categories from App - By the User - from App
	try:
		user_id = str(request.POST['userid'])
		category_name = request.POST['categoryname']
		usr = Users.objects.get(pk=user_id)
		category = Categories(category_name=category_name, type_of_category='custom', created_by=usr)
		category.save()
		category_id=str(category.pk)
		records = []
		recArr = {}
		recArr['status']=1
		recArr['id']=category_id
		recArr['addedby']=usr.email
		recArr['userid']=user_id
		recArr['type']='custom'
		recArr['category']=category_name
		records.append(recArr)
		tophone = json.dumps(records)	
		return HttpResponse(tophone)
	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def addpost(request):
	#rendering the add post page
	#HTML in soapbox/templates/
	t = get_template('addpost.html')
	html = t.render(Context({}))
	return HttpResponse(html)

@csrf_exempt
def addpostrec(request):
	#code to add posts
	try:
		#Fetching Categories list in which the podcast has to be posted
		categories = request.POST.getlist('category')
		description = request.POST['description']
		user_id = str(request.POST['userid'])
		#Fetching the Uploaded File
		upfile = request.FILES['upfile']
		
		#Get the uploaded FileName
		filename = upfile.name;
		todb = settings.MEDIA_URL+"posts/"+filename;

		#Path - Where to store the uploaded file
		uploaded = settings.BASE_DIR+"/media/posts/"+filename
		output_file = open(settings.BASE_DIR+"/media/posts/"+filename, "w")
		
		#Store Uploaded File
		output_file.write(upfile.read())
		output_file.close()

		#Give Permissions to the uploaded File so that it is accessible from anywhere
		#os.chmod(settings.BASE_DIR+"/media/posts/"+filename, 0644)
		subprocess.call(['chmod', '0777', uploaded]) #change permissions for uploaded file
		
		#Fetching the User Details who Posted the Podcast
		usr = Users.objects.get(pk=user_id)

		#Saving the Post
		post = Posts(post_file_url=todb, post_description=description, user_by=usr)
		post.save()

		#fetching the Post ID of the uploaded Post
		post_id = str(post.pk)

		#Storing the record for categories in which the Post is posted
		for category in categories:
			categ = Categories.objects.get(pk=category)
			postcat = PostCategories(category=categ, post=post)
			postcat.save()
			
		t = get_template('display.html')
		html = t.render(Context({'categories': categories, 'description': description, 'filename': filename}))
		return HttpResponse(html)

	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def webautotimer(request):
	#Web service for Auto Length Timer to play the podcast
	atimer = PodcastTimer.objects.values_list('timer',flat=True)
	timer=[]
	tim ={}
	tim['status']=1
	for t in atimer:
		timer.append(t)

	tim['autolength']=timer
	data = json.dumps(tim)
	return HttpResponse(data)

@csrf_exempt
def webaddpost(request):
	#Web servie to add Podcasts - Audio Posts
	try:
		#Fetching Categories list in which the podcast has to be posted
		categories = request.POST.getlist('category')
		description = request.POST['description']
		user_id = str(request.POST['userid'])
		#Fetching the Uploaded File
		upfile = request.FILES['upfile']
		
		#Get the uploaded FileName
		filename = upfile.name;
		todb = settings.MEDIA_URL+"posts/"+filename;

		#Path - Where to store the uploaded file
		uploaded = settings.BASE_DIR+"/media/posts/"+filename
		output_file = open(settings.BASE_DIR+"/media/posts/"+filename, "w")
		
		#Store Uploaded File
		output_file.write(upfile.read())
		output_file.close()

		#Give Permissions to the uploaded File so that it is accessible from anywhere
		#os.chmod(settings.BASE_DIR+"/media/posts/"+filename, 0644)
		subprocess.call(['chmod', '0777', uploaded]) #change permissions for uploaded file
		
		#Fetching the User Details who Posted the Podcast
		usr = Users.objects.get(pk=user_id)

		#Saving the Post
		post = Posts(post_file_url=todb, post_description=description, user_by=usr)
		post.save()

		#fetching the Post ID of the uploaded Post
		post_id = str(post.pk)

		#Storing the record for categories in which the Post is posted
		for category in categories:
			categ = Categories.objects.get(pk=category)
			postcat = PostCategories(category=categ, post=post)
			postcat.save()

		#Generating JSON Response for Mobile App
		records = []
		recArr = {}
		recArr['status']=1
		recArr['podcast_id']=post_id
		recArr['filepath']=todb
		records.append(recArr)
		tophone = json.dumps(records)

		#t = get_template('display.html')
		#html = t.render(Context({'categories': categories, 'description': description, 'filename': filename}))
		return HttpResponse(tophone)

	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def webpodcastlistened(request, post_id):
	#Web Service to increment the podcast listen value - Podcasts Listens (Like Youtube Views)
	try:
		#post_id=3
		podcast = Posts.objects.get(pk=post_id)
		try:
			#Checking if a Podcast has been Listened earlier - If a record for that Podcast exists in existing records
			pListen = PostListens.objects.get(post=podcast)
			#Fetching Existing Listens
			tListen = pListen.num_listens;
			#Incrementing Listens
			tListen = tListen+1
			pListen.num_listens = tListen
			#Updating and Saving Listens
			pListen.save()
			records = []
			recArr = {}
			recArr['status']=1
			recArr['listens']=tListen
			records.append(recArr)
			#Generating JSON Response
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except PostListens.DoesNotExist:
			#adding the first Listen for Podcast if does not exists
			pListen = PostListens(post=podcast, num_listens=1)
			pListen.save()
			records = []
			recArr = {}
			recArr['status']=1
			recArr['listens']=1
			#Generating JSON Response
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except Exception as e:
			records = []
			recArr = {}
			recArr['status']=0
			recArr['error']=e.message
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def webpodcastlistenedtotal(request, post_id):
	#Web Service to increment the podcast listen value - Podcasts Listens (Like Youtube Views)
	try:
		#post_id=3
		podcast = Posts.objects.get(pk=post_id)
		try:
			#Checking if a Podcast has been Listened earlier - If a record for that Podcast exists in existing records
			pListen = PostListens.objects.get(post=podcast)
			#Fetching Existing Listens
			tListen = pListen.num_listens;
			records = []
			recArr = {}
			recArr['status']=1
			recArr['listens']=tListen
			records.append(recArr)
			#Generating JSON Response
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except PostListens.DoesNotExist:
			records = []
			recArr = {}
			recArr['status']=0
			recArr['listens']=0
			#Generating JSON Response
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except Exception as e:
			records = []
			recArr = {}
			recArr['status']=0
			recArr['error']=e.message
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone) 

def webpodcastliked(request, post_id):
	#Web Service to increment the podcast like value - Podcasts Likes
	try:
		#post_id=3
		podcast = Posts.objects.get(pk=post_id)
		try:
			#Checking if a Podcast has been Lisked earlier - If a record for that Podcast exists in existing records
			pLike = PostLikes.objects.get(post=podcast)
			#Fetching Existing Likes
			tLike = pLike.num_likes;
			#Incrementing Likes
			tLike = tLike+1
			pLike.num_likes = tLike
			#Updating and Saving Likes
			pLike.save()
			records = []
			recArr = {}
			recArr['status']=1
			recArr['likes']=tLike
			records.append(recArr)
			#Generating JSON Response
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except PostLikes.DoesNotExist:
			#adding the first Like for Podcast if does not exists
			pLike = PostLikes(post=podcast, num_likes=1)
			pLike.save()
			records = []
			recArr = {}
			recArr['status']=1
			recArr['likes']=1
			#Generating JSON Response
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except Exception as e:
			records = []
			recArr = {}
			recArr['status']=0
			recArr['error']=e.message
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def webpodcastlikedtotal(request, post_id):
	#Web Service to increment the podcast like value - Podcasts Likes
	try:
		#post_id=3
		podcast = Posts.objects.get(pk=post_id)
		try:
			#Checking if a Podcast has been Lisked earlier - If a record for that Podcast exists in existing records
			pLike = PostLikes.objects.get(post=podcast)
			#Fetching Existing Likes
			tLike = pLike.num_likes;
			records = []
			recArr = {}
			recArr['status']=1
			recArr['likes']=tLike
			records.append(recArr)
			#Generating JSON Response
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except PostLikes.DoesNotExist:
			records = []
			recArr = {}
			recArr['status']=1
			recArr['likes']=0
			#Generating JSON Response
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except Exception as e:
			records = []
			recArr = {}
			recArr['status']=0
			recArr['error']=e.message
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def webpodcastshared(request, post_id):
	#Web Service to increment the podcast share value - Podcasts Shared
	try:
		#post_id=3
		podcast = Posts.objects.get(pk=post_id)
		try:
			#Checking if a Podcast has been Shared earlier - If a record for that Podcast exists in existing records
			pShare = PostShares.objects.get(post=podcast)
			#Fetching Existing Shares
			tShare = pShare.num_shares;
			#Incrementing Likes
			tShare = tShare+1
			pShare.num_shares = tShare
			#Updating and Saving Shares
			pShare.save()
			records = []
			recArr = {}
			recArr['status']=1
			recArr['shares']=tShare
			records.append(recArr)
			#Generating JSON Response
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except PostShares.DoesNotExist:
			#adding the first Share for Podcast if does not exists
			pShare = PostShares(post=podcast, num_shares=1)
			pShare.save()
			records = []
			recArr = {}
			recArr['status']=1
			recArr['shares']=1
			#Generating JSON Response
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except Exception as e:
			records = []
			recArr = {}
			recArr['status']=0
			recArr['error']=e.message
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def webpodcastsharedtotal(request, post_id):
	#Web Service to increment the podcast share value - Podcasts Shared
	try:
		#post_id=3
		podcast = Posts.objects.get(pk=post_id)
		try:
			#Checking if a Podcast has been Shared earlier - If a record for that Podcast exists in existing records
			pShare = PostShares.objects.get(post=podcast)
			#Fetching Existing Shares
			tShare = pShare.num_shares;
			records = []
			recArr = {}
			recArr['status']=1
			recArr['shares']=tShare
			records.append(recArr)
			#Generating JSON Response
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except PostShares.DoesNotExist:
			records = []
			recArr = {}
			recArr['status']=1
			recArr['shares']=0
			#Generating JSON Response
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

		except Exception as e:
			records = []
			recArr = {}
			recArr['status']=0
			recArr['error']=e.message
			records.append(recArr)
			tophone = json.dumps(records)
			return HttpResponse(tophone)

	except Exception as e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

def streampodcast(request, post_id):
	#Web service to Stream Podcast on app - as per thr ID in Posts Table
	try:
		podcast=Posts.objects.select_related('user_by').get(pk=post_id)
		podcast_url=request.META['HTTP_HOST']+podcast.post_file_url;
		podcast_description=podcast.post_description
		date_posted=podcast.posted_on
		date_posted=date_posted.strftime('%b %d, %Y')
		time_posted=podcast.posted_at
		time_posted=time_posted.strftime('%H:%M')
		
		email=podcast.user_by.email

		usr=PersonalDetails.objects.select_related('user').get(user_id=podcast.user_by.id)
		first_name=usr.first_name
		last_name=usr.last_name
		age=usr.age
		state=usr.state
		city=usr.city

		#podcast = Posts.objects.select_related('user_by').get(pk = post_id)
		#return HttpResponse(podcast.user_by.email)
		
		posts=[]
		postsArr={}
		postsArr['url']=podcast_url
		postsArr['description']=podcast_description
		postsArr['date']=date_posted
		postsArr['time']=time_posted
		posts.append(postsArr)

		users=[]
		usersArr={}
		usersArr['id']=podcast.user_by.id
		usersArr['email']=email
		usersArr['firstname']=first_name
		usersArr['lastname']=last_name
		#usersArr['age']=age
		#usersArr['state']=state
		#usersArr['city']=city
		users.append(usersArr)


		records = []
		recArr = {}
		recArr['status']=1
		#recArr['path']=podcast_url
		records.append(recArr)
		records.append(posts)
		records.append(users)
		tophone = json.dumps(records)
		return HttpResponse(tophone)

	except Posts.DoesNotExist:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']='Does Not Exists'
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone)
	except Exception, e:
		records = []
		recArr = {}
		recArr['status']=0
		recArr['error']=e.message
		records.append(recArr)
		tophone = json.dumps(records)
		return HttpResponse(tophone) 

def testapp2(request):
    t='hello i am here'
        
    return render(request, "testapp.html")