from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from ces2013_broker.views import audio_proxy

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns=patterns('')

# ... the rest of your URLconf goes here ...

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^content/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATICFILES_DIRS[0],
        }),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        
   )

urlpatterns += patterns('',
    # Examples:

    url(r'^api/', include('api.urls')),
    
    
    url(r'^audio_proxy.wav$',audio_proxy),

    #url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap.sitemaps}),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

    
    url(r'^(?P<url>[A-Za-z0-9\/\-_]+)$', flatpage,name="ces2013_broker_flatpage"),
        
    
    
)

