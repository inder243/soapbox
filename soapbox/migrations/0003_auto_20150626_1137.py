# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soapbox', '0002_auto_20150619_0549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user',
        ),
        migrations.RemoveField(
            model_name='groupuserscategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='groupuserscategory',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='usr',
        ),
        migrations.DeleteModel(
            name='PodcastTimer',
        ),
        migrations.RemoveField(
            model_name='postcategories',
            name='category',
        ),
        migrations.RemoveField(
            model_name='postcategories',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postlikes',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postlistens',
            name='post',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='user_by',
        ),
        migrations.RemoveField(
            model_name='postshares',
            name='post',
        ),
        migrations.RemoveField(
            model_name='userfollowers',
            name='follower_id',
        ),
        migrations.RemoveField(
            model_name='userfollowers',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='userimage',
        ),
        migrations.RemoveField(
            model_name='userstatus',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userstatus',
            name='usrst',
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='GroupUsersCategory',
        ),
        migrations.DeleteModel(
            name='PersonalDetails',
        ),
        migrations.DeleteModel(
            name='PostCategories',
        ),
        migrations.DeleteModel(
            name='PostLikes',
        ),
        migrations.DeleteModel(
            name='PostListens',
        ),
        migrations.DeleteModel(
            name='Posts',
        ),
        migrations.DeleteModel(
            name='PostShares',
        ),
        migrations.DeleteModel(
            name='UserFollowers',
        ),
        migrations.DeleteModel(
            name='UserImage',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.DeleteModel(
            name='UserStatus',
        ),
    ]
