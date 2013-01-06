from django.db import models
from account.managers import UserProfileManager
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class UserProfile(models.Model):  
    """
    Extended user data. Contains User preferences, a relationship to a profile
    image, and basic information.
    """
    user = models.OneToOneField(User)  
    #other fields here
    slug = models.SlugField()
        
    
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    about = models.TextField(null=True)
    telephone = models.CharField(max_length=15,null=True)
    

    
    objects = UserProfileManager()
    
    
    #django standards:
    def get_absolute_url(self):
        return "/account/profile/%s" % self.slug


    #python standards:
    def __str__(self):  
        return "%s's profile" % self.user  
    
    def __unicode__(self):  
        return self.__str__()  
    
    
#=====django rigging======
admin.site.register((UserProfile))