from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from twitpng.views import post_longtweet, tweet_sent

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^twauth/', include('twython_django_oauth.urls')),
    url(r'^post_longtweet', post_longtweet),
    url(r'^tweetsent', tweet_sent),
    url(r'^$', TemplateView.as_view(template_name="home.html")),
)
