'''
Created on Oct 24, 2012

@author: matt
'''
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm
import re
from account.models import UserProfile
from django.forms.fields import CharField

def _(string):
    return string;

class SignInForm(AuthenticationForm):
    """
    Form for signing in
    """
    username = CharField(label=("Username or Email"), max_length=100)
    
    
    




class SignUpForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        
       
        
        self.error_messages = dict({
            'duplicate_username': _("A user with that username already exists."),
            'password_mismatch': _("The two password fields didn't match."),
            'duplicate_email': _("Sorry, that email is already in use."),
        }.items())
        
        super(SignUpForm,self).__init__(*args, **kwargs)
    
    
    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
    
    
    email = forms.EmailField(label=_("Email"), max_length=80,
        
        help_text = _("Required. 80 characters or fewer. Valid email address only."),
        error_messages = {
            'invalid': _("Please use a valid email address.")})
    
    password1 = forms.CharField(widget=forms.PasswordInput(),help_text = _("Required."),)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat your password",help_text = _("Required."),)
    
    def clean_password(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password1']
    
    def clean(self,*args, **kwargs):
        
        self.clean_password()
        return super(SignUpForm, self).clean(*args, **kwargs)
    
    class Meta:
        pass;
    
    pass

class ProfileForm(ModelForm):
   
    
    def clean_telephone(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        telephone = self.cleaned_data["telephone"]        
        return re.sub(r'[^0-9]',"",telephone)
    
    telephone = forms.RegexField(label=_("Phone"), max_length=15,
        regex=r'^[0-9\(\)\s\-\.]+$',
        required=False,
        help_text = _("Optional. 15 characters or fewer. Valid phone number only."),
        error_messages = {
            'invalid': _("Please use a valid phone number.")})
    
    
    
    class Meta:
        model = UserProfile
        exclude = ("user","slug",)
    
    pass

#class SignUpFormCombined(SignUpForm,ProfileForm):
    #pass;
