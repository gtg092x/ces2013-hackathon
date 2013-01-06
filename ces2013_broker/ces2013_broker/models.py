'''
Created on Nov 21, 2012

@author: matt
'''
from django.contrib.flatpages.models import FlatPage
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import models
 
class SiteFlatPage(FlatPage):
    def get_absolute_url(self):
        return self.url;
    
    
    
    def save(self, force_insert=False, force_update=False):        
        self.enable_comments = False
        self.registration_required = False
        if(len(self.template_name) == 0):
            self.template_name = 'flatpages/{0}.html'.format(self.url.strip("/"));
        super(SiteFlatPage, self).save(force_insert, force_update)
    class Meta:
        proxy=True
        
class IncomingMessage(models.Model):
    created_on = models.DateTimeField(auto_now_add=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,blank=True)
    message = models.TextField()
    viewed = models.BooleanField(default=False,blank=True)
    to_number = models.CharField(max_length=10)
    from_number = models.CharField(max_length=10)
    
class OutgoingMessage(models.Model):
    created_on = models.DateTimeField(auto_now_add=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,blank=True)
    message = models.TextField()
    sent = models.BooleanField(default=False,blank=True)
    to_number = models.CharField(max_length=10)
    from_number = models.CharField(max_length=10)
        
admin.site.register(SiteFlatPage)
admin.site.register(User)
admin.site.register(Site)
admin.site.register(Token)
admin.site.register(IncomingMessage)
admin.site.register(OutgoingMessage)
