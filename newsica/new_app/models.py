from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class news(models.Model):
	title=models.CharField(max_length=100)
	content=models.TextField(max_length=2000)
	user=models.ForeignKey(User)
	def __unicode__(self):
		return self.title
	def get_absolute_url(self):
		return "/news/get/%i/" % self.id

class top_n(models.Model):
	title=models.CharField(max_length=100)
	content=models.TextField(max_length=1000)
	upload = models.FileField(upload_to='static/img/uploads/')
	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateField(default=datetime.date.today())
    def __str__(self):
       return self.user.username

