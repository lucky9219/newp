from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.core.context_processors import csrf
from forms import *
from models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def main_page(request):
	new_s=news.objects.all()
	top=top_n.objects.all()
	variables = RequestContext(request, {
    'new_s': new_s,
    'top':top
  	})
	return render_to_response('main_page.html', variables)

def register_user(request):
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
                messages.add_message(request, messages.INFO, "Invitation successfully sent")
                return HttpResponseRedirect('/registration/register_success')
            except:
            	messages.add_message(request, messages.INFO, "Invitation not send successfully.Try again later")
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
def user_page(request):
	return HttpResponseRedirect('/')