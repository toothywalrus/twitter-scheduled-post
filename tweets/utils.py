import os
import os.path

from django.conf import settings

import twitter
import importlib

os.chdir(os.path.abspath('tweets/templates/partials'))


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


def get_form_id(form_class):
    """
    Receives instance of the 'ModelForm' and returns 'id' for this form
    to render in HTML.
    """
    # return "%s_form" % (form_instance._meta.model.__name__.lower(),)
    return "%s_form" % (form_class._meta.model.__name__.lower(),)


def get_serializer_class(model_name):
    """
    Returns serializer class for model 'model_name'.
    """
    import serializers
    module = importlib.import_module('tweets.models')
    model = getattr(module, model_name)

    serializer_name = "".join([model.__name__, 'Serializer'])
    return getattr(serializers, serializer_name)


def get_viewset_class(model_name):
    import views
    return getattr(views, ''.join([model_name, 'ViewSet']))


def get_form_class(model_name):
    import forms
    return getattr(forms, ''.join([model_name, 'Form']))


def get_viewset_name(model_name):
    return ''.join([model_name, 'ViewSet'])


def get_model_class(model_name):
    import models
    return getattr(models, model_name)

INFO_NAMES = ('Tweet', 'TimedTweet', 'PostTweetSet', 'PeriodicTweet',
              'Interval', 'TwitterUser',)


def get_info_names():
    return INFO_NAMES


def get_info_models():
    """
    Returns list of models for using in InfoView etc.
    """
    import models

    models = [getattr(models, name) for name in INFO_NAMES]

    return models


def get_info_forms():
    return [get_form_class(name) for name in INFO_NAMES]


def get_info_viewsets():

    viewsets = [get_viewset_class(name) for name in INFO_NAMES]
    return viewsets


def get_partials(exclude=None):
    if exclude is None:
        exclude = ['modal.html']
    partials = []
    for dirname, dirnames, filenames in os.walk('.'):
        for filename in list(set(filenames) - set(exclude)):
            root = os.path.basename(os.path.abspath(os.getcwd()))
            partial_url = os.path.normpath(
                os.path.join(root, os.path.basename(dirname), filename))
            partial_base = os.path.basename(dirname)
            if partial_base is not '.':
                if partial_base[-1] is 's':
                    partial_base = partial_base[:-1]
                to_join = [os.path.splitext(filename)[0], '-',
                           partial_base,
                           os.path.splitext(filename)[1]]
            else:
                to_join = [filename]
            partial_id = ''.join(to_join)
            partials.append((partial_id, partial_url,))
    return partials


def is_posted(tweet_pk, user_pk):
    from .models import Post
    return Post.objects.filter(tweet=tweet_pk, user=user_pk).exists()


def mark_posted(tweet_pk, user_pk):
    from .models import Post, Tweet, TwitterUser
    tweet = Tweet.objects.get(pk=tweet_pk)
    user = TwitterUser.objects.get(pk=user_pk)
    Post.objects.create(tweet=tweet, user=user)


def is_already_posted(tweet_pk, users_qs):
    from .models import Post
    tweet_users = Post.objects.filter(tweet=tweet_pk).\
        values_list('user', flat=True)
    our_users = users_qs.values_list('id', flat=True)
    return set(our_users) in set(tweet_users)


def set_already_posted(model, pk):
    inst = model.objects.get(pk=pk)
    inst.already_posted = True
    inst.save(update_fields=['already_posted'])
