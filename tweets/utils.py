from django.conf import settings

import twitter
import importlib


def get_api(consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET):
    """
    Returns an Api instance from 'twitter' module with given requivisites.
    """
    print "api call"
    api = twitter.Api(
        consumer_key, consumer_secret, access_token_key, access_token_secret)
    return api


def get_model_name(model_name):
    """
    Returns name for the model 'model_name' for use in Angular.

    """
    return "".join([model_name[0].lower(), model_name[1:]])


def get_resource_name(model_name):
    """
    Returns name for the resource used in Restangularb y the 'model_name'.
    Actually is pluralized version of 'model_name'.
    """
    return "".join([model_name.lower(), "s"])


def get_form_id(form_instance):
    """
    Receives instance of the 'ModelForm' and returns 'id' for this form
    to render in HTML.
    """
    return "%s_form" % (form_instance._meta.model.__name__.lower(),)


def get_serializer_class(model_name):
    """
    Returns serializer class for model 'model_name'.
    """
    import serializers
    module = importlib.import_module('tweets.models')
    model = getattr(module, model_name)

    serializer_name = "".join([model.__name__, 'Serializer'])
    return getattr(serializers, serializer_name)


def get_info_models():
    """
    Returns list of models for using in InfoView etc.
    """
    from .models import Tweet, PostTweetSet, TimedTweet, PeriodicTweet,\
        Interval

    return [Tweet, TimedTweet, PostTweetSet, PeriodicTweet,
            Interval]
