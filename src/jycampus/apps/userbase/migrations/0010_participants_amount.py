# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-16 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userbase', '0009_participants_fee_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='participants',
            name='amount',
            field=models.TextField(blank=True, help_text='Amount paid by the Participant', null=True, verbose_name='amount'),
        ),
    ]
