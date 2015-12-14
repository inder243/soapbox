# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class SoapboxAppcategory(models.Model):
    category = models.CharField(max_length=255)
    channel = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'soapbox_appcategory'


class SoapboxAppusers(models.Model):
    apikey = models.CharField(max_length=255)
    socialid = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dateofbirth = models.DateField()
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    profilepic = models.CharField(max_length=255)
    created_at = models.DateField()
    #modified_at = models.DateField(null=True, blank=True)
	#phonenumber = models.IntegerField()
    voicemessage = models.CharField(max_length=255)
    usertype = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'soapbox_appusers'
		
class SoapboxDevicetoken(models.Model):
	userid = models.IntegerField()
	devicetype = models.IntegerField()
	devicetoken = models.CharField(max_length=255)
	
	class Meta:
		managed = False
		db_table = 'soapbox_devicetoken'


class SoapboxCategories(models.Model):
    channel_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
   # modified_at = models.TimeField()
    type_of_channel = models.IntegerField()
    created_by_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'soapbox_categories'
		
class SoapboxPosts(models.Model):
	userid = models.IntegerField()
    post_file_url = models.CharField(max_length=255)
    posted_on = models.DateField()
    posted_at = models.TimeField()
	modified_at = models.DateField()
    class Meta:
        managed = False
        db_table = 'soapbox_posts'


class SoapboxChatmod(models.Model):
    jabber_id = models.BigIntegerField()
    jabber_password = models.CharField(max_length=72)
#    juser = models.ForeignKey('SoapboxUsers')

    class Meta:
        managed = False
        db_table = 'soapbox_chatmod'


class SoapboxComments(models.Model):
    description = models.TextField()
    comment = models.TextField(blank=True, null=True)
    type_of_post = models.CharField(max_length=7)
    comment_on = models.DateField()
    comment_at = models.TimeField()
#    user = models.ForeignKey('SoapboxUsers')

    class Meta:
        managed = False
        db_table = 'soapbox_comments'
		
class SoapboxConnectiontablesocialid(models.Model):

    userid = models.IntegerField()
    socialsitename = models.CharField(max_length=255)
    socialid = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'soapbox_connectiontablesocialid'


class SoapboxGroupuserscategory(models.Model):
    category = models.ForeignKey(SoapboxCategories)
#    user = models.ForeignKey('SoapboxUsers')

    class Meta:
        managed = False
        db_table = 'soapbox_groupuserscategory'


class SoapboxPersonaldetails(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(blank=True, null=True)
    age = models.SmallIntegerField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    profile_img = models.CharField(max_length=250)
#    user = models.ForeignKey('SoapboxUsers')

    class Meta:
        managed = False
        db_table = 'soapbox_personaldetails'


class SoapboxPodcasttimer(models.Model):
    timer = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'soapbox_podcasttimer'


class SoapboxPostcategories(models.Model):
    category = models.ForeignKey(SoapboxCategories)
#    post = models.ForeignKey('SoapboxPosts')

    class Meta:
        managed = False
        db_table = 'soapbox_postcategories'


class SoapboxPostlikes(models.Model):
    num_likes = models.IntegerField()
#    post = models.ForeignKey('SoapboxPosts')

    class Meta:
        managed = False
        db_table = 'soapbox_postlikes'


class SoapboxPostlistens(models.Model):
    num_listens = models.IntegerField()
#    post = models.ForeignKey('SoapboxPosts')

    class Meta:
        managed = False
        db_table = 'soapbox_postlistens'




class SoapboxPostshares(models.Model):
    num_shares = models.IntegerField()
    post = models.ForeignKey(SoapboxPosts)

    class Meta:
        managed = False
        db_table = 'soapbox_postshares'
		
class SoapboxSubscribechannel(models.Model):
    userid = models.IntegerField()
    channelid = models.IntegerField()
    issubscribe = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'soapbox_subscribechannel'


#class SoapboxUserfollowers(models.Model):
#    follower_id = models.ForeignKey('SoapboxUsers')
#    user_id = models.ForeignKey('SoapboxUsers')

#    class Meta:
#        managed = False
#        db_table = 'soapbox_userfollowers'


#class SoapboxUserimage(models.Model):
#    profilepic = models.CharField(max_length=150)
#    user = models.ForeignKey('SoapboxUsers')
#    userimage = models.ForeignKey('SoapboxUsers', unique=True)
#
#    class Meta:
#        managed = False
#        db_table = 'soapbox_userimage'


#class SoapboxUsers(models.Model):
#    username = models.CharField(max_length=50)
#    email = models.CharField(max_length=254)
#    password = models.CharField(max_length=50)
#    status = models.SmallIntegerField()
#    user_type = models.CharField(max_length=10)
#    registered_thru = models.CharField(max_length=20)
#
#    class Meta:
#        managed = False
#        db_table = 'soapbox_users'


class SoapboxUserstatus(models.Model):
    about = models.TextField()
 #   user = models.ForeignKey(SoapboxUsers)
 #   usrst = models.ForeignKey(SoapboxUsers, unique=True)

    class Meta:
        managed = False
        db_table = 'soapbox_userstatus'
