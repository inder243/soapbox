from django.db import models
# Create your models here.

class Users(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50)
	email = models.EmailField(null=False)
	password = models.CharField(max_length=50)
	status = models.SmallIntegerField(null=False)
	user_type = models.CharField(max_length=10, null=False)
	registered_thru = models.CharField(max_length=20, null=False)

class PersonalDetails(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users, related_name='users', related_query_name='usr', on_delete=models.CASCADE)
	first_name = models.CharField(max_length=40, null=False)
	last_name = models.CharField(max_length=30)
	dob = models.DateField(null=True)
	age = models.SmallIntegerField()
	state = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	profile_img = models.CharField(max_length=250)

class ChatMod(models.Model):
	juser = models.ForeignKey(Users, related_name='jusers', related_query_name='jusr', on_delete=models.CASCADE)
	jabber_id = models.BigIntegerField()
	jabber_password = models.CharField(max_length=72)

class UserStatus(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users, related_name='usrstats', related_query_name='usrs', on_delete=models.CASCADE)
	about = models.TextField(null=False)
	usrst = models.OneToOneField(Users, related_name='usrstat')

class UserImage(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users, related_name='usersim', related_query_name='usrimg', on_delete=models.CASCADE)
	profilepic = models.CharField(max_length=150,null=False)
	userimage = models.OneToOneField(Users, related_name='usrimage')

class UserFollowers(models.Model):
	user_id = models.ForeignKey(Users, related_name='usrid', related_query_name='followusr', on_delete=models.CASCADE)
	follower_id = models.ForeignKey(Users, related_name='usrfl', related_query_name='usrfollower', on_delete=models.CASCADE)

class Categories(models.Model):
	id = models.AutoField(primary_key=True)
	category_name = models.CharField(max_length=50, null=False)
	created_by = models.ForeignKey(Users, related_name='usrcatcreate', related_query_name='catusr', on_delete=models.CASCADE)
	#usrcat = models.OneToOneField(Users, related_name='usrcateg')
	created_on = models.DateField(auto_now=True)
	created_at = models.TimeField(auto_now=True)
	type_of_category = models.CharField(max_length=10)

#To store the users to a custom Group created by another user
class GroupUsersCategory(models.Model):
	category = models.ForeignKey(Categories, related_name='usrcategry', related_query_name='grpusr', on_delete=models.CASCADE)
	user = models.ForeignKey(Users, related_name='grpusrs', related_query_name='gusrid', on_delete=models.CASCADE)

class Posts(models.Model):
	id = models.AutoField(primary_key=True)
	post_file_url = models.CharField(max_length=150, null=False)
	post_title = models.CharField(max_length=150)
	post_description = models.TextField()
	posted_on = models.DateField(auto_now=True)
	posted_at = models.TimeField(auto_now=True)
	user_by = models.ForeignKey(Users, related_name='usrpost', related_query_name='postusr', on_delete=models.CASCADE)
	#postuser = 	models.ManyToManyField(Users, related_name='pstusrs')

class PostCategories(models.Model):
	id = models.AutoField(primary_key=True)
	category = models.ForeignKey(Categories, related_name='categtype', related_query_name='cattype', on_delete=models.CASCADE)
	post = models.ForeignKey(Posts, related_name='post', related_query_name='posts', on_delete=models.CASCADE)

class PostLikes(models.Model):
	post = models.ForeignKey(Posts, related_name='likepost', related_query_name='postlik', on_delete=models.CASCADE)
	num_likes = models.IntegerField()

class PostListens(models.Model):
	post = models.ForeignKey(Posts, related_name='listenpost', related_query_name='postlisten', on_delete=models.CASCADE)
	num_listens = models.IntegerField()

class PostShares(models.Model):
	post = models.ForeignKey(Posts, related_name='sharepost', related_query_name='postshare', on_delete=models.CASCADE)
	num_shares = models.IntegerField()

class Comments(models.Model):
	id = models.AutoField(primary_key=True)
	description = models.TextField(null=False)
	comment = models.TextField(null=True)
	type_of_post = models.CharField(max_length=7, null=False)
	user = models.ForeignKey(Users, related_name='cmtusr', related_query_name='usrcmr', on_delete=models.CASCADE)
	comment_on = models.DateField(auto_now=True)
	comment_at = models.TimeField(auto_now=True)

class PodcastTimer(models.Model):
	id = models.AutoField(primary_key=True)
	timer = models.IntegerField(null=False)

	def __str__(self):
		return "%s" % (self.timer)