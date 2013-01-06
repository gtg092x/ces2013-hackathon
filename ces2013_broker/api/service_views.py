'''
Created on Nov 23, 2012

@author: matt
'''
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from account.forms import SignUpForm, SignInForm
from api.service_serializers import SignUpSerializer
from account.views import SignUpView
from rest_framework.exceptions import APIException, ParseError
from django.forms.models import ModelForm
from api.serializers import UserSerializer
from django.contrib.auth import authenticate, logout, login
from rest_framework.authtoken.models import Token

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'sign-up': reverse('sign-up', request=request),
        'login': reverse('login', request=request),
        'logout': reverse('logout', request=request),
    })
    
class ApiFormView(APIView):
    
    def get_form_class(self):
        return self.form_class
    
    def bound_form_dict(self,form):
        
        fields = [{"name":field.html_name,"label":unicode(field.label),
                   "errors":[error for error in field.errors],
                   "hint":field.help_text,} 
                  for field in form]
        return {"form":{"fields":fields,
                        #"nonfield_errors":[unicode(error) for error in form.errors],
                        "is_valid":form.is_valid()}}
    
    def initial_form_dict(self,):
        form = self.get_form_class()();
        fields = [{"name":field.html_name,"label":unicode(field.label),"hint":field.help_text,} for field in form]
        return {"form":{"fields":fields}}
    
    
    def form_valid(self,form):
        if issubclass(form.__class__,ModelForm):
            return Response({"model":form.save(commit=False),"success":True})
        else:
            return Response(self.bound_form_dict(form));
    
    def form_invalid(self,form):
        return Response(self.bound_form_dict(form));
    
    
    def get(self, request, format=None):
        """
        Returns data for a signup form
        """       
        return Response(self.initial_form_dict())
    
    def post(self, request, format=None):
        """
        Returns data for a signup form
        """
        form = self.get_form_class()(data=request.DATA);
        
        if(form.is_valid()):
            return self.form_valid(form);
        else:        
            return self.form_invalid(form);
    
    pass;


def session_info(user,request):
    serializer = UserSerializer(user)
    data = serializer.data
    data["session"]=request.session.session_key;
    data["pk"] = serializer.object.pk
    return data;  

    
class SignUp(ApiFormView):
    """ 
    API Endpoint for a form
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    form_class = SignUpForm

    def form_valid(self,form):
        
        user = User.objects.create_user(form.cleaned_data["email"], 
                                        form.cleaned_data["email"],
                                        form.cleaned_data["password1"],)
        user.save();
        user = authenticate(username=form.cleaned_data["email"], 
                            password=form.cleaned_data["password1"])
        if user is not None:
            
            logout(self.request._request);
            login(self.request._request, user)
        
        
        return Response(session_info(user,self.request));
    
   
        

class SignIn(ApiFormView):
    
    form_class = SignInForm
    
    """
    API endpoint for logging in
    """
    permission_classes = (permissions.AllowAny,)
    def form_valid(self, form,):
        user = authenticate(username=form.cleaned_data["username"], 
                            password=form.cleaned_data["password"])
        if user is not None:
            login(self.request._request, user)        
            return Response(session_info(user,self.request));
        
        return super(SignIn,self).form_invalid(form);
    
class AuthToken(ApiFormView):
    
    form_class = SignInForm
    
    """
    API endpoint for logging in
    """
    permission_classes = (permissions.AllowAny,)
    def form_valid(self, form,):
        user = authenticate(username=form.cleaned_data["username"], 
                            password=form.cleaned_data["password"])
        if user is not None:
            token = Token.objects.get_or_create(user=user)        
            return Response({"token":token[0].key});
        
        return super(SignIn,self).form_invalid(form);
    
    

class SignOut(generics.GenericAPIView):
    """
    API endpoint for logging out
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self,request,format=None):
        logout(self.request._request);
        return Response({"result":"success"});



