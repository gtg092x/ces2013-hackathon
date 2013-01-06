'''
Created on Oct 24, 2012

@author: matt
'''
from django.conf.urls import patterns, include, url
from account.views import SignOutView, SignInView, SignUpView, SelfProfileView,\
    EditProfileView,OAuthRedirectView 




# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('account.views',
    # Examples:
    #url(r'social/',include('social_auth.urls')),
    url(r'^signout$', SignOutView.as_view()),
    url(r'^signin$', SignInView.as_view(),name="account_signin"),
    url(r'^signup$', SignUpView.as_view(),name="account_signup"),
    url(r'^profile$', SelfProfileView.as_view(),name="account_self_profile"),
    url(r'^profile/(?P<slug>.*)$', EditProfileView.as_view(),name="account_profile"),

    
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
