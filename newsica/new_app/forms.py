from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    def clean_email(self):
    	email = self.cleaned_data["email"]
    	return email
#    	try:
#        	User._default_manager.get(email=email)
#    	except User.DoesNotExist:
#        	return email
#    	raise forms.ValidationError('duplicate email')

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
    content=forms.CharField(
        label='news',
        widget=forms.Textarea(attrs={'size':64})
        )
    tags=forms.CharField(
        label='TAGS',
        required=True,
        widget=forms.TextInput(attrs={'size':64})
        )