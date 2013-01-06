from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer,\
    IncomingMessageSerializer, OutgoingMessageSerializer
from ces2013_broker.models import IncomingMessage, OutgoingMessage
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['GET'])
def api_root(request, format=None):
    """
    Welcome to your API
    """
    return Response({
        'users': reverse('user-list', request=request),
        'groups': reverse('group-list', request=request),
    })

class UserList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    model = User
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = User
    serializer_class = UserSerializer

class GroupList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = Group
    
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = Group
    serializer_class = GroupSerializer
    
class IncomingMessageList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of Incoming Messages.
    """
    model = IncomingMessage
    serializer_class = IncomingMessageSerializer
    permission_classes = (AllowAny,)
    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.
        """
        
        backend = self.filter_backend()
        qs= backend.filter_queryset(self.request, queryset, self)
        for im in qs:
            im.viewed=True;
            im.save();
            pass;
        return qs;
    

class IncomingMessageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single Incoming Message.
    """
    model = IncomingMessage
    
class OutgoingMessageList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of Outgoing Messages.
    """
    permission_classes = (AllowAny,)
    model = OutgoingMessage
    serializer_class = OutgoingMessageSerializer
    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.
        """
        
        backend = self.filter_backend()
        qs= backend.filter_queryset(self.request, queryset, self)
        for om in qs:
            om.sent=True;
            om.save();
            pass;
        return qs;
    

class OutgoingMessageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single Outgoing Message.
    """
    model = OutgoingMessage
    