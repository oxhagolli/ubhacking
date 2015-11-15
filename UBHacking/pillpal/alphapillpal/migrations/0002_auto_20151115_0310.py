# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alphapillpal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='time',
            field=models.TextField(null=True),
        ),
    ]
