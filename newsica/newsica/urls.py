from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
urlpatterns = [
    # Examples:
    # url(r'^$', 'newsica.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
url(r'^search/', include('haystack.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','new_app.views.main_page',),
     url(r'^login/$','django.contrib.auth.views.login',),
   url(r'^accounts/login/$','django.contrib.auth.views.login',),
      url(r'^logout/$','new_app.views.logout_page',),
     url(r'^signup/$','new_app.views.register_user',),
        url(r'^user/$','new_app.views.user_page',),
     url(r'^accounts/confirm/(?P<activation_key>\w+)/','new_app.views.register_confirm'),
     url(r'^registration/register_success',TemplateView.as_view(template_name="registration/register_success.html")),
     url('', include('social.apps.django_app.urls', namespace='social')),
  url(r'^save/$','new_app.views.save_news_page',),
 
]
