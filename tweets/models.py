from datetime import datetime


from django.db import models
from django.db.models import signals

from django.contrib.auth import get_user_model

from rest_framework.renderers import UnicodeJSONRenderer

from djcelery.models import PeriodicTask, PeriodicTasks, IntervalSchedule

from django_sse.redisqueue import send_event


from .tasks import post_timed_tweet, start_tweet_set
import utils


class TwitterUser(models.Model):
    username = models.CharField()
    consumer_key = models.CharField()
    consumer_secret = models.CharField()
    access_token_key = models.CharField()
    access_token_secret = models.CharField()


class TaskScheduler(PeriodicTask):

    """
    Proxy-model for PeriodicTask model, used to create, destroy and control
    it. PeriodicTask instance with field 'enabled' set to 'true' gets started
    to execute in Celery, because of the way MQ used by Djangular, Kombu
    works.
    """

    class Meta:
        proxy = True

    @classmethod
    def create(cls, task_name, period, every, args="[]", kwargs="{}"):
        """
        Creates an instance of Djangular PerioicTask for task 'task_name'
        with some interval('period', 'every').
        """
        periodic_task_name = "%s_%s" % (task_name, datetime.now())
        interval, _ = IntervalSchedule.objects.get_or_create(
            period=period, every=every)
        ts = cls(name=periodic_task_name, task=task_name,
                 interval=interval, args=args, kwargs=kwargs, enabled=False)
        return ts

    def start(self):
        """
        Make task enabled.
        """
        self.enabled = True
        self.save()

    def stop(self):
        """
        Make task disabled.
        """
        self.enabled = False
        self.save()

    def terminate(self):
        """
        Delete task from database.
        """
        self.stop()
        self.delete()

# Djangular uses signal 'PeriodicTasks.changed' to notify
# MQ about changes.
signals.pre_save.connect(PeriodicTasks.changed, sender=TaskScheduler)


class Postable(models.Model):
    already_posted = models.BooleanField(default=False, editable=False)
    # po st_time = models.DateTimeField()

    class Meta:
        abstract = True


class LiveModel(models.Model):

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
        super(LiveModel, self).save(*args, **kwargs)
        self.send_event(event)

    def delete(self, *args, **kwargs):
        self.send_event('deleted')
        super(LiveModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class Tweet(LiveModel):

    """
    Simple tweet model.
    """

    status = models.TextField(max_length=140)
    user = models.ForeignKey(get_user_model())
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "'%s' by %s" % (self.status, self.user)


class PostTweetSet(LiveModel):

    """
    Represents some set of tweets which might be
    posted every given period of time(periodic tweets).
    Must be started at given time (start_time field).
    """

    interval = models.ForeignKey(IntervalSchedule)
    description = models.CharField(max_length=200)
    start_time = models.DateTimeField()

    def next_tweet(self):
        """
        Selects next non-posted periodic tweet with lowest priority from set.
        If there is no such tweet, returns 'None'.
        """
        try:
            nt = self.tweets.filter(
                already_posted=False).order_by('priority')[0]
        except IndexError:
            nt = None
        return nt

    def save(self, *args, **kwargs):
        super(PostTweetSet, self).save(*args, **kwargs)

        start_tweet_set.apply_async(
            args=[self.pk, self.interval.period, self.interval.every],
            eta=self.start_time)

    def __unicode__(self):
        return "%s, %s, start time: %s" % \
            (self.description, self.interval, self.start_time)


class TimedTweet(LiveModel, Postable):

    """
    Tweet that needs to be posted at specified time 'post_time'.
    """
    tweet = models.ForeignKey(Tweet, related_name='timedtweets')
    post_time = models.DateTimeField()

    def __unicode__(self):
        return "Post '%s' at %s" % (self.tweet, self.post_time)

    def save(self, *args, **kwargs):
        pk = self.pk
        super(TimedTweet, self).save(*args, **kwargs)
        if pk is None:
            post_timed_tweet.apply_async(args=[self.pk], eta=self.post_time)


class PeriodicTweet(LiveModel, Postable):

    """
    Tweet that belongs to some set of tweets to post every period of time
    (PostTweetSet). Has its own priority in this set - 'priority'.
    """
    tweetset = models.ForeignKey(PostTweetSet, related_name='tweets')
    tweet = models.ForeignKey(Tweet)
    priority = models.IntegerField()
    posted_on = models.DateTimeField(editable=False, null=True)

    def __unicode__(self):
        return '%s' % (self.tweet,)
