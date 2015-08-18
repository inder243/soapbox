# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(max_length=50)),
                ('created_on', models.DateField(auto_now=True)),
                ('created_at', models.TimeField(auto_now=True)),
                ('type_of_category', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('description', models.TextField()),
                ('type_of_post', models.CharField(max_length=7)),
                ('comment_on', models.DateField(auto_now=True)),
                ('comment_at', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupUsersCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(related_query_name=b'grpusr', related_name='usrcategry', to='soapbox.Categories')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.SmallIntegerField()),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PodcastTimer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timer', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PostCategories',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('category', models.ForeignKey(related_query_name=b'cattype', related_name='categtype', to='soapbox.Categories')),
            ],
        ),
        migrations.CreateModel(
            name='PostLikes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_likes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PostListens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_listens', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('post_file_url', models.CharField(max_length=150)),
                ('post_description', models.TextField()),
                ('posted_on', models.DateField(auto_now=True)),
                ('posted_at', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostShares',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_shares', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserFollowers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('profilepic', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name=b'Username')),
                ('password', models.CharField(max_length=50)),
                ('status', models.SmallIntegerField()),
                ('user_type', models.CharField(max_length=10)),
                ('registered_thru', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('about', models.TextField()),
                ('user', models.ForeignKey(related_query_name=b'usrs', related_name='usrstats', to='soapbox.Users')),
                ('usrst', models.OneToOneField(related_name='usrstat', to='soapbox.Users')),
            ],
        ),
        migrations.AddField(
            model_name='userimage',
            name='user',
            field=models.ForeignKey(related_query_name=b'usrimg', related_name='usersim', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='userimage',
            name='userimage',
            field=models.OneToOneField(related_name='usrimage', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='userfollowers',
            name='follower_id',
            field=models.ForeignKey(related_query_name=b'usrfollower', related_name='usrfl', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='userfollowers',
            name='user_id',
            field=models.ForeignKey(related_query_name=b'followusr', related_name='usrid', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='postshares',
            name='post',
            field=models.ForeignKey(related_query_name=b'postshare', related_name='sharepost', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='posts',
            name='user_by',
            field=models.ForeignKey(related_query_name=b'postusr', related_name='usrpost', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='postlistens',
            name='post',
            field=models.ForeignKey(related_query_name=b'postlisten', related_name='listenpost', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='postlikes',
            name='post',
            field=models.ForeignKey(related_query_name=b'postlik', related_name='likepost', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='postcategories',
            name='post',
            field=models.ForeignKey(related_query_name=b'posts', related_name='post', to='soapbox.Posts'),
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='user',
            field=models.ForeignKey(related_query_name=b'usr', related_name='users', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='usr',
            field=models.OneToOneField(related_name='usrdet', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='groupuserscategory',
            name='user',
            field=models.ForeignKey(related_query_name=b'gusrid', related_name='grpusrs', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(related_query_name=b'usrcmr', related_name='cmtusr', to='soapbox.Users'),
        ),
        migrations.AddField(
            model_name='categories',
            name='created_by',
            field=models.ForeignKey(related_query_name=b'catusr', related_name='usrcatcreate', to='soapbox.Users'),
        ),
    ]
