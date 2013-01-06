'''
Created on Nov 23, 2012

@author: matt
'''
from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import UserList, UserDetail, GroupList, GroupDetail,\
    IncomingMessageList, IncomingMessageDetail, OutgoingMessageList,\
    OutgoingMessageDetail
from api.service_views import SignUp, SignIn, SignOut, AuthToken
import rest_framework

 
urlpatterns = patterns('api.views',
    url(r'^$', 'api_root'),
    url(r'^users$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)$', UserDetail.as_view(), name='user-detail'),
    url(r'^groups$', GroupList.as_view(), name='group-list'),
    url(r'^groups/(?P<pk>\d+)$', GroupDetail.as_view(), name='group-detail'),
     
    url(r'^incoming-messages$', IncomingMessageList.as_view(), name='incoming-message-list'),
    url(r'^incoming-message/(?P<pk>\d+)$', IncomingMessageDetail.as_view(), name='incoming-message-detail'),
    url(r'^outgoing-messages$', OutgoingMessageList.as_view(), name='outgoing-message-list'),
    url(r'^outgoing-message/(?P<pk>\d+)$', OutgoingMessageDetail.as_view(), name='outgoing-message-detail'),
     
    #service
    url(r'^service/auth/sign-up$', SignUp.as_view(), name='sign-up', ),
    url(r'^service/auth/sign-in$', SignIn.as_view(), name='sign-in', ),
    url(r'^service/auth/sign-out$', SignOut.as_view(), name='sign-out', ),
    url(r'^service/auth/api-token$', AuthToken.as_view(), name='auth-token',)
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api','xml','yaml','html'])

# Default login/logout views
urlpatterns += patterns('',
    url(r'^browse-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    #url(r'^token-auth/', 'rest_framework.authtoken.obtain_auth_token'),
)
