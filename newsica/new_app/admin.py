from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(news)
admin.site.register(top_n)
admin.site.register(UserProfile)
admin.site.register(user_news)
admin.site.register(Tag)
