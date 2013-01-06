'''
Created on Nov 23, 2012

@author: matt
'''
from django.contrib.auth.models import Group, User, Permission
from rest_framework import serializers
from ces2013_broker.models import OutgoingMessage, IncomingMessage


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups',)
        
class OutgoingMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OutgoingMessage
        fields = ('message', 'to_number', 'from_number',)
        
class IncomingMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IncomingMessage
        fields = ('message', 'to_number', 'from_number',)

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.ManySlugRelatedField(
        slug_field='codename',
        queryset=Permission.objects.all()
    )

    class Meta:
        model = Group
        fields = ('url', 'name', 'permissions')