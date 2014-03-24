from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

import utils

from .views import InfoView

router = DefaultRouter(trailing_slash=False)

for name in utils.get_info_names():
    router.register(utils.get_resource_name(
        name), utils.get_viewset_class(name))

urlpatterns = patterns('',
                       url(r'^info$', InfoView.as_view(), name='info'),
                       url(r'^', include(router.urls)),
                       )
