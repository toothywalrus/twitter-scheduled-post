from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'celery_test.views.home', name='home'),
                       # url(r'^celery_test/', include('celery_test.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', TemplateView.as_view(
                           template_name='index.html'), name='home'),
                       url(r'^edit$', TemplateView.as_view(
                           template_name='editor.html'), name='editor'),
                       url(r'^do_task$', 'progress.views.do_task', name='do_task'),
                       url(r'^poll_state$',
                           'progress.views.poll_state', name='poll_state'),

                       url(r'^test_async$',
                           'progress.views.test_async', name='test_async'),

                       url(r'^api-auth/', include(
                           'rest_framework.urls', namespace='rest_framework')),
                       url(r'^api/', include('celery_test.api.urls')),
                       url(r'^tweets/', include('tweets.urls')),
                       url(r'^facebook/', include('django_facebook.urls')),
                       url(r'^accounts/', include(
                           'django_facebook.auth_urls')),

                       )
