"""iapptech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from soapbox import views
from soapbox import soapboxwebservice
from soapboxadmin import views as adminviews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register-user'),
    url(r'^register-test/$', views.register, name='register-user'),
    url(r'^addcat/$', views.addcat),
    url(r'^addpost/$', views.addpost),
    url(r'^addpostrec/$', views.addpostrec),
    url(r'^addcategories/$', views.addcategories),
    url(r'^mobileregemail/$', views.mobwebregemail),
    url(r'^mobileregsocial/$', views.mobwebregsocial),
    url(r'^autotimer/$', views.webautotimer),
    url(r'^podcastlistens/(?P<post_id>[0-9]+)/$', views.webpodcastlistened),
    url(r'^podcastlikes/(?P<post_id>[0-9]+)/$', views.webpodcastliked),
    url(r'^podcastshares/(?P<post_id>[0-9]+)/$', views.webpodcastshared),
    url(r'^listentotal/(?P<post_id>[0-9]+)/$', views.webpodcastlistenedtotal),
    url(r'^likestotal/(?P<post_id>[0-9]+)/$', views.webpodcastlikedtotal),
    url(r'^sharedtotal/(?P<post_id>[0-9]+)/$', views.webpodcastsharedtotal),
    url(r'^podcast/(?P<post_id>[0-9]+)/$', views.streampodcast),
    url(r'^soapbox/$', adminviews.index, name='admin-index'),
    url(r'^soapbox/index/$', adminviews.index, name='admin-index'),
    url(r'^soapbox/login/$', adminviews.login, name='admin-login'),
    url(r'^logout/$', adminviews.logout, name='admin-logout'),
    url(r'^manageusers/$', adminviews.manageusers, name='admin-manage-users'),
    url(r'^manageposts/$', adminviews.manageposts, name='admin-manage-posts'),
    url(r'^managecategories/$', adminviews.managecategories, name='admin-manage-categories'),
    url(r'^manageautolength/$', adminviews.manageautolength, name='admin-manage-autolength'),
    url(r'^manageprofile/$', adminviews.manageprofile, name='admin-manage-profile'),
    url(r'^editprofile/$', adminviews.editprofile, name='admin-edit-profile'),
    url(r'^authenticate/$', adminviews.authenticate, name='admin-authenticate'),

    #For Testing Purpose
   # url(r'^testapp/$', views.testapp),
    url(r'^testapp2/$', views.testapp2),
	
	
	# for webservice
	 url(r'^appregister/$', soapboxwebservice.appRegister),
	 url(r'^applogin/$', soapboxwebservice.appLogin),
	 url(r'^channelSuggestions/$', soapboxwebservice.channelSuggestions),
	 url(r'^serachcategory/$', soapboxwebservice.serachCategory),
	 url(r'^uploadfile/$', soapboxwebservice.uploadfile),
	 url(r'^connectSocialMedia/$', soapboxwebservice.connectSocialMedia),
	 url(r'^postAudioMessage/$', soapboxwebservice.postAudioMessage),
	 url(r'^subscribechannel/$', soapboxwebservice.subscribechannel),
	 url(r'^follow/$', soapboxwebservice.follow),
	 url(r'^postAudioReplyMessage/$', soapboxwebservice.postAudioReplyMessage),
	 url(r'^userPostList/$', soapboxwebservice.userPostList),
	 url(r'^headerinfo/$', soapboxwebservice.headerinfo),
	 url(r'^like/$', soapboxwebservice.like),
	 url(r'^getPopularPostList/$', soapboxwebservice.getPopularPostList),
	 url(r'^getUserList/$', soapboxwebservice.getUserList),
	 url(r'^getFollowingPostList/$', soapboxwebservice.getFollowingPostList),
	 url(r'^postReplyOther/$', soapboxwebservice.postReplyOther),
	 
]