# Create your views here.
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth import logout, authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from account.forms import ProfileForm, SignInForm, SignUpForm
from account.models import UserProfile


class SignOutView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, **kwargs):
        returnUrl = (self.request.GET.get("ref","/"))+"?message=You+have+been+logged+out"
        logout(self.request);
        return returnUrl


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class LoginRedirectMixin(object):
    
    redirect_field_name="next"  
        

    def get_success_url(self):
        if self.success_url:            
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, "/account/profile")        
        
        print(redirect_to)
        print(self.redirect_field_name)
        return redirect_to

     
class SignInView(LoginRedirectMixin,FormView):
    form_class = SignInForm
    
    
    def get_template_names(self):
        return "account/signin.html";
    pass;

class OAuthRedirectView(TemplateView):
    
    
    def get_template_names(self):
        return "account/signin.html";
    pass;




class SignUpView(LoginRedirectMixin,FormView):
    def get_form_class(self):
        return SignUpForm;
    
    
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(FormView, self).dispatch(*args, **kwargs)
    
    def get_template_names(self):
        return "account/signup.html";

    
    def form_valid(self, form):
        
        user = User.objects.create_user(form.cleaned_data["email"], 
                                        form.cleaned_data["email"],
                                        form.cleaned_data["password1"],)
        user.save();
        user = authenticate(username=form.cleaned_data["email"], 
                            password=form.cleaned_data["password1"])
        if user is not None:
            
            logout(self.request);
            login(self.request, user)
            
            
            return super(SignUpView, self).form_valid(form)
        
        else:
            
            return super(FormView, self).form_invalid(form)
    

class EditProfileView(LoginRequiredMixin,UpdateView):
    form_class = ProfileForm
    
    model = UserProfile
    
    def form_valid(self, form):
        form.save();
        return super(EditProfileView,self).form_valid(form);
    
    def get(self, request, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.helper.form_action = reverse("account_profile",kwargs={"slug":slugify(self.request.user)});
        form.instance=self.object;
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)
    
    
    def get_template_names(self):
        return "account/profile.html";
    pass;


class SelfProfileView(LoginRequiredMixin,RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, **kwargs):
        returnUrl = reverse("account_profile",kwargs={"slug":slugify(self.request.user)});
        
        return returnUrl



class PasswordChangeView(FormView):
    def get_form_class(self):
        return PasswordChangeForm;
    pass;

class UserRegistrationView(FormView):
    def get_form_class(self):
        return UserCreationForm;
    pass;
