from rest_framework.renderers import UnicodeJSONRenderer

from django_sse.redisqueue import send_event

import utils


class LiveMixin(object):

    """
    Base class for all models, which should send events to client
    about their updates
    """

    def send_event(self, event):
        data = {}
        data.update({'item': utils.get_serializer_class(
            self.__class__.__name__)(instance=self).data})
        data.update(
            {'model_name': utils.get_model_name(self.__class__.__name__)})
        send_event(event, UnicodeJSONRenderer()
                   .render(data=data), channel="stream")

    def save(self, *args, **kwargs):
        event = 'saved' if self.pk is None else 'changed'
        super(LiveMixin, self).save(*args, **kwargs)
        self.send_event(event)

    def delete(self, *args, **kwargs):
        self.send_event('deleted')
        super(LiveMixin, self).delete(*args, **kwargs)
