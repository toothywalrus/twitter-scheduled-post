from django.views.generic import TemplateView

from rest_framework import viewsets, generics, permissions
from rest_framework.renderers import UnicodeJSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response


from django_sse.redisqueue import send_event


from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet, Interval
from .forms import TweetForm, PostTweetSetForm, PeriodicTweetForm, \
    TimedTweetForm, IntervalForm
from .utils import get_resource_name, get_form_id, get_serializer_class,\
    get_info_models


class MainHomePage(TemplateView):

    """
    Home page for our app.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainHomePage, self).get_context_data(**kwargs)

        forms_list = [
            TweetForm, PostTweetSetForm, PeriodicTweetForm, TimedTweetForm,
            IntervalForm]
        forms = dict((get_form_id(form()), form()) for form in forms_list)
        context.update(forms)

        return context


class ReadNestedWriteFlatMixin(object):

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super(
            ReadNestedWriteFlatMixin, self).\
            get_serializer_class(*args, **kwargs)
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            serializer_class.Meta.depth = 0
        return serializer_class


class BaseViewSet(viewsets.ModelViewSet):
    pass


class TweetViewSet(BaseViewSet):
    model = Tweet


class TweetTimedTweetsList(generics.ListCreateAPIView):
    model = TimedTweet
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        queryset = super(TweetTimedTweetsList, self).get_queryset()
        return queryset.filter(tweet__pk=self.kwargs.get('pk'))


class TimedTweetViewSet(BaseViewSet):
    model = TimedTweet


class PeriodicTweetViewSet(BaseViewSet):
    model = PeriodicTweet


class PostTweetSetViewSet(BaseViewSet):
    model = PostTweetSet


class IntervalViewSet(BaseViewSet):
    model = Interval


class InfoView(APIView):

    """
    View for getting a bulk of models information at once.
    """

    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        models_list = get_info_models()
        info = {get_resource_name(model.__name__):
                get_serializer_class(model.__name__)(
                model.objects.all(), many=True).data
                for model in models_list}
        return Response(info)
