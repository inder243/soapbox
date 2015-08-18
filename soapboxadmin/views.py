from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.cache import cache_control
from django.db import transaction
from array import array
from datetime import date
from django.conf import settings
from soapbox.models import Users, PersonalDetails, UserStatus, UserImage, UserStatus, UserFollowers, Categories, GroupUsersCategory, Posts, PostCategories, PostLikes, PostListens, PostShares, Comments, PodcastTimer
from django.core import serializers #for serialization to and from JSON, XML
import md5, json, os, MySQLdb, os, subprocess
# Create your views here.

def index(request):
	if 'username' in request.session:
		t = get_template('soapboxadmin/index.html')
		html = t.render(Context({}))
		return HttpResponse(html)
	else:
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def login(request):
	t = get_template('soapboxadmin/login.html')
	html = t.render(Context({}))
	return HttpResponse(html)

@csrf_exempt
def authenticate(request):
	username=request.POST['username']
	password=md5.new(request.POST['password']).hexdigest()
	try:
		users = Users.objects.get(username=username)
		passwd = users.password
		if password==passwd:
			usrType=users.user_type
			if usrType=="admin":
				request.session['username']=username
				request.session.modified = True
				return HttpResponse("ok")
			else:
				return HttpResponse("no")
		else:
			return HttpResponse("pwd")
	except Users.DoesNotExist:
		return HttpResponse("usr")

def logout(request):
	if 'username' in request.session:
		del request.session['username']
		request.session.modified = True
		request.session.clear()
		request.session.modified = True
		request.session.flush()
		request.session.modified = True
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)
	else:
		request.session.clear()
		request.session.modified = True
		request.session.flush()
		request.session.modified = True
		request.session.modified = True
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def manageusers(request):
	if 'username' in request.session:
		#request.session.modified = True
		try:
			users=PersonalDetails.objects.select_related('user').all();
			t = get_template('soapboxadmin/manageusers.html')
			html = t.render(Context({'userslist':users}))
			return HttpResponse(html)
			#request.session.modified = Truesponse(html)
		except PersonalDetails.DoesNotExist:
			t = get_template('soapboxadmin/manageusers.html')
			html = t.render(Context())
			return HttpResponse(html)
	else:
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def manageposts(request):
	if 'username' in request.session:
		#request.session.modified = True
		try:
			allposts = []
			mposts = {}
			categoriesAll=""
			posts = Posts.objects.select_related('user_by').all()
			for post in posts:
				mposts['post_id']=str(post.id)
				mposts['user_email']=str(post.user_by.email)
				mposts['post_description']=str(post.post_description)
				pcategs = PostCategories.objects.select_related('category').filter(post=post)
				for categs in pcategs:
					categoriesAll+=str(categs.category.category_name)+","

				catlen=len(categoriesAll)-1
				mposts['categories']=categoriesAll[:catlen].split(',')
				allposts.append(mposts)
				categoriesAll=""
				mposts={}

			t = get_template('soapboxadmin/manageposts.html')
			html = t.render(Context({'allposts':allposts}))
			return HttpResponse(html)
			#return HttpResponse(allposts)
			#request.session.modified = Truesponse(html)
		except Posts.DoesNotExist:
			t = get_template('soapboxadmin/manageposts.html')
			html = t.render(Context())
			return HttpResponse(html)
	else:
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def managecategories(request):
	if 'username' in request.session:
		#request.session.modified = True
		try:
			categories = Categories.objects.select_related('created_by').all()

			t= get_template('soapboxadmin/managecategories.html')
			html = t.render(Context({'categories': categories}))
			return HttpResponse(html)
		except Categories.DoesNotExist:
			t= get_template('soapboxadmin/managecategories.html')
			html = t.render(Context({}))
			return HttpResponse(html)

	else:
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def manageautolength(request):
	if 'username' in request.session:
		try:
			podcast = PodcastTimer.objects.all()

			t= get_template('soapboxadmin/manageautolength.html')
			html = t.render(Context({'podcast': podcast}))
			return HttpResponse(html)
		except Categories.DoesNotExist:
			t= get_template('soapboxadmin/manageautolength.html')
			html = t.render(Context({}))
			return HttpResponse(html)

	else:
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def manageprofile(request):
	if 'username' in request.session:
		try:
			user_name = request.session['username']
			user_detail = Users.objects.get(username=user_name)
			t= get_template('soapboxadmin/manageprofile.html')
			html = t.render(Context({'user_detail': user_detail}))
			#html = t.render(Context({'user_name': user_name}))
			return HttpResponse(html)
		except Categories.DoesNotExist:
			t= get_template('soapboxadmin/manageprofile.html')
			html = t.render(Context({}))
			return HttpResponse(html)

	else:
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)

@csrf_exempt
def editprofile(request):
	if 'username' in request.session:
		try:
			user_name = request.session['username']

			if'submit' in request.POST:
				Users.objects.filter(username=user_name).update(email = request.POST['email'])
				return HttpResponseRedirect('/soapbox/manageprofile/')
			
			user_detail = Users.objects.get(username=user_name)
			t= get_template('soapboxadmin/editprofile.html')
			html = t.render(Context({'user_detail': user_detail}))
			#html = t.render(Context({'user_name': user_name}))
			return HttpResponse(html)

		except Categories.DoesNotExist:
			t= get_template('soapboxadmin/editprofile.html')
			html = t.render(Context({}))
			return HttpResponse(html)

	else:
		t = get_template('soapboxadmin/login.html')
		html = t.render(Context({}))
		return HttpResponse(html)