from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from pagedown.widgets import PagedownWidget
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    def clean_email(self):
    	email = self.cleaned_data["email"]
    	return email
       	try:
           	User._default_manager.get(email=email)
       	except User.DoesNotExist:
           	return email
       	raise forms.ValidationError('duplicate email')

    def save(self, commit=True):        
    	user = super(RegistrationForm, self).save(commit=False)
    	user.email = self.cleaned_data['email']
    	if commit:
        	user.is_active = False # not active until he opens activation link
        	user.save()

    	return user



class save_news(forms.Form):
    title=forms.CharField(
        label='title',
        widget=forms.TextInput(attrs={'size':64},
            )
        )
    content=forms.CharField(widget=PagedownWidget)
    tags=forms.CharField(
        label='tags',
        required=True,
        widget=forms.TextInput(attrs={'size':64})
        )
    image=forms.ImageField(label='image',required=False)


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    def clean_email(self):
        email = self.cleaned_data["email"]
        return email

class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Password'}))
    new_password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Confirm Password'}))

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2
