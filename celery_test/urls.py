from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from django_sse.redisqueue import RedisQueueView

from tweets.views import MainHomePage

from .apiauth import ObtainAuthToken, ObtainLogout, ObtainUser

admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^api-auth/', include(
                           'rest_framework.urls', namespace='rest_framework')),

                       url(r'^api-token/login/(?P<backend>[^/]+)/$',
                           ObtainAuthToken.as_view()),
                       url(r'^api-token/user/', ObtainUser.as_view()),
                       url(r'^api-token/logout/', ObtainLogout.as_view()),

                       url(r'^tweets/', include('tweets.urls')),


                       url(r'^experiments$', TemplateView.as_view(
                           template_name='experiments.html'),
                       name='experiments'),
                       url(r'^stream/$', RedisQueueView.as_view(
                           redis_channel="stream"),
                           name='stream'),
                       url(r'^$', MainHomePage.as_view(), name='home'),
                       )


urlpatterns += staticfiles_urlpatterns()
