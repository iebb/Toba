# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Todo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=100, blank=True, default='')
    markdown = models.TextField(blank=True, default='')
    progress = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User', related_name='todo', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created', 'priority')
