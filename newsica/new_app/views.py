from django.shortcuts import render_to_response, get_object_or_404,redirect
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.core.context_processors import csrf
from forms import *
from django.db.models.query_utils import Q
from models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, random
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset      
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template import loader
from django.views.generic import *
from django.contrib.auth import get_user_model

def main_page(request):
	new_s=news.objects.all()
	top=top_n.objects.all()
	variables = RequestContext(request,{'new_s': new_s,'top':top,'user':request.user})
	return render_to_response('main_page.html', variables)

def register_user(request):
  if request.user.is_active:
      return HttpResponseRedirect('/'
       #'/user/%s/' % request.user.username
     )
  else:  
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid(): 
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today().date()

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile                                                                                                                                  
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            24 hours http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

            try:
            	send_mail(email_subject, email_body, 'myemail@example.com',
                [email], fail_silently=False)
                messages.add_message(request, messages.INFO, "Verification mail sent successfully to provided email")
                return HttpResponseRedirect('/registration/register_success')
            except:
            	messages.add_message(request, messages.INFO, "Unable to send verification email!!Please check your network and emailid.")
    else:
        args['form'] = RegistrationForm()

    return render_to_response('registration/register.html', args, context_instance=RequestContext(request))







def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires==datetime.datetime.today().date():
        user = user_profile.user
    	user.is_active = True
    	user.save()
    	return render_to_response('registration/confirm.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    else:
    	return render_to_response('registration/confirm_expired.html')


def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')


@login_required
def about(request):
  return render_to_response('about.html')

@login_required
def save_news_page(request):
  if request.method == 'POST':
    form = save_news(request.POST,request.FILES)
    if form.is_valid():
     if 'image' in request.FILES:
      obj, created = user_news.objects.get_or_create(
      user=request.user,title=form.cleaned_data['title'],content=form.cleaned_data['content'],upload=request.FILES['image'])
     else:
      obj, created = user_news.objects.get_or_create(
      user=request.user,title=form.cleaned_data['title'],content=form.cleaned_data['content'])
     # Update bookmark title.
     tag_names=form.cleaned_data['tags']
     # If the bookmark is being updated, clear old tag list.
     if not created:
        obj.tag_set.clear()
     # Create new tag list.

     for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        obj.tag_set.add(tag)
     # Save bookmark to database.
     obj.save()

     return HttpResponseRedirect('/'
       #'/user/%s/' % request.user.username
     )
  else:
    form = save_news()
  variables = RequestContext(request, {'form': form})
  return render_to_response('save_news.html', variables)

@login_required
def newss(request):
    var=user_news.objects.all()
    time=timezone.now()
    variables=RequestContext(request,{'var':var,'time':time})
    return render_to_response('user_page.html',variables)


class ResetPasswordRequestView(FormView):
        template_name = "registration/password_reset_form.html"
        form_class = PasswordResetRequestForm
        @staticmethod
        def validate_email_address(email):
            try:
                validate_email(email)
                return True
            except ValidationError:
                return False
        def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
             data= form.cleaned_data["email"]
             if self.validate_email_address(data) is True:            
                associated_users= User.objects.filter(Q(email=data)|Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                            c = {
                                'email': user.email,
                                'domain': request.META['HTTP_HOST'],
                                'site_name': 'your site',
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'user': user,
                                'token': default_token_generator.make_token(user),
                                'protocol': 'http',
                                }
                            subject_template_name='registration/password_reset_subject.txt' 
                            # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                            email_template_name='registration/password_reset_email.html'    
                            # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                            subject = loader.render_to_string(subject_template_name, c)
                            # Email subject *must not* contain newlines
                            subject = ''.join(subject.splitlines())
                            email = loader.render_to_string(email_template_name, c)
                            try:
                              send_mail(subject, email, 'myemail@example.com' , [user.email], fail_silently=False)
                              messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                              return HttpResponseRedirect('/reset/done/')  
                            except:
                              messages.error(request, 'check your network connectivity Or')  
                              break    
             messages.error(request, 'Check The email address address you entered')
             return render_to_response('registration/password_reset_error.html',context_instance=RequestContext(request))

class PasswordResetConfirmView(FormView):
    template_name = "registration/password_reset_confirm.html"
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return HttpResponseRedirect('/login')
            else:
                messages.error(request, 'Password reset has not been unsuccessful.Try again')
                return HttpResponseRedirect('/reset')
        else:
            messages.error(request,'The reset password link is no longer valid.Try again')
            return HttpResponseRedirect('/reset')

@login_required
def my_page(request):
    var=user_news.objects.filter(user=request.user)
    time=timezone.now()
    variables=RequestContext(request,{'var':var,'time':time})
    return render_to_response('user_page.html',variables)


def user1(request,username):
  try:
    user=User.objects.get(username=username)
  except:
    raise Http404('Requested user not found')
  time=timezone.now()
  var=user.user_news_set.all()
  variables=RequestContext(request,{'var':var,'time':time,'user':username})
  return render_to_response('user1.html',variables)

def dis(request,id):
  try:
    var=news.objects.get(id=id)
  except:
    raise Http404('Requested news not found')
  time=timezone.now()
  variables=RequestContext(request,{'var':var,'time':time})
  return render_to_response('dis.html',variables)

def dis_user(request,id):
  try:
    var=user_news.objects.get(id=id)
  except:
    raise Http404('Requested news not found')
  time=timezone.now()
  variables=RequestContext(request,{'var':var,'time':time})
  return render_to_response('dis1.html',variables)


def delet(request,id):
  var=user_news.objects.get(id=id)
  if var.user!=request.user:
    raise Http404("you don't have permission to delete this")
  if request.method=="POST":
    var.delete()
    return HttpResponseRedirect('/')
    messages.success(request, "successfully deleted")
  variables=RequestContext(request,{'var':var})
  return render_to_response("confirm_delet.html",variables)