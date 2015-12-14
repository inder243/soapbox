# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soapbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postlikes',
            name='post',
            field=models.ForeignKey(related_query_name=b'postlik', related_name='likepost', to='soapbox.Posts'),
        ),
        migrations.AlterField(
            model_name='postlistens',
            name='post',
            field=models.ForeignKey(related_query_name=b'postlisten', related_name='listenpost', to='soapbox.Posts'),
        ),
        migrations.AlterField(
            model_name='postshares',
            name='post',
            field=models.ForeignKey(related_query_name=b'postshare', related_name='sharepost', to='soapbox.Posts'),
        ),
    ]
