from datetime import datetime


from django.db import models
from django.db.models import signals


from djcelery.models import PeriodicTask, PeriodicTasks, IntervalSchedule


from .tasks import post_timed_tweet, start_tweet_set
from .mixins import LiveMixin
import utils


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
        Creates an instance of Djangular PeriodicTask for task 'task_name'
        with some interval('period', 'every').
        """
        periodic_task_name = "%s_%s" % (task_name, datetime.now())
        interval, _ = IntervalSchedule.objects.get_or_create(
            period=period, every=every)
        ts = cls(name=periodic_task_name, task=task_name,
                 interval=interval, args=args, kwargs=kwargs, enabled=False)
        ts.save()
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

    class Meta:
        abstract = True


class Interval(LiveMixin, IntervalSchedule):
    pass


class TwitterUser(models.Model):
    username = models.CharField(max_length=30)
    consumer_key = models.CharField(max_length=128)
    consumer_secret = models.CharField(max_length=128)
    access_token_key = models.CharField(max_length=128)
    access_token_secret = models.CharField(max_length=128)

    def get_api(self):
        return utils.get_api(self.consumer_key, self.consumer_secret,
                             self.access_token_key, self.access_token_secret)

    def __unicode__(self):
        return "%s" % self.username


class Tweet(LiveMixin, models.Model):

    """
    Simple tweet model.
    """

    status = models.TextField(max_length=140, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "'%s' at %s" % (self.status, self.created_on)


class Post(models.Model):
    tweet = models.ForeignKey(Tweet, related_name="posts")
    user = models.ForeignKey(TwitterUser, related_name="posts")
    posted_on = models.DateTimeField(editable=False, null=True)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now()
        super(Post, self).save()

    class Meta:
        unique_together = ('tweet', 'user',)


class PostTweetSet(LiveMixin, models.Model):

    """
    Represents some set of tweets which might be
    posted every given period of time(periodic tweets).
    Must be started at given time (start_time field).
    """

    def __init__(self, *args, **kwargs):
        super(PostTweetSet, self).__init__(*args, **kwargs)

    interval = models.ForeignKey(IntervalSchedule)
    description = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    users = models.ManyToManyField(TwitterUser, related_name='posttweetsets')

    periodic_task = models.OneToOneField(PeriodicTask, null=True, blank=True)

    def next_periodic_tweet(self):
        """
        Selects next non-posted periodic tweet with lowest priority from set.
        If there is no such tweet, returns 'None'.
        """
        try:
            nt = self.periodictweets.filter(
                already_posted=False).order_by('priority')[0]
        except IndexError:
            nt = None
        return nt

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(PostTweetSet, self).save(*args, **kwargs)
            self.save(*args, **kwargs)
        else:
            periodic_task = TaskScheduler.create(
                'tweets.tasks.post_next_tweet', self.interval.period,
                self.interval.every, args="[" + '"%s"' % str(self.pk) + "]")
            PostTweetSet.objects.filter(pk=self.pk).update(
                periodic_task=periodic_task)
            start_tweet_set.apply_async(
                args=[periodic_task.pk],
                eta=self.start_time)

    def delete(self, *args, **kwargs):
        self.periodic_task.delete()
        super(PostTweetSet, self).delete(*args, **kwargs)

    def __unicode__(self):
        return "%s, %s, start time: %s" % \
            (self.description, self.interval, self.start_time)


class TimedTweet(LiveMixin, Postable):

    """
    Tweet that needs to be posted at specified time 'post_time'.
    """
    tweet = models.ForeignKey(Tweet, related_name='timedtweets')
    post_time = models.DateTimeField()
    users = models.ManyToManyField(
        TwitterUser, related_name='timedtweets')

    def __unicode__(self):
        return "Post '%s' at %s" % (self.tweet, self.post_time)

    def save(self, *args, **kwargs):
        pk = self.pk
        super(TimedTweet, self).save(*args, **kwargs)
        if pk is None:
            post_timed_tweet.apply_async(
                args=[self.pk], eta=self.post_time)


class PeriodicTweet(LiveMixin, Postable):

    """
    Tweet that belongs to some set of tweets to post every period of time
    (PostTweetSet). Has its own priority in this set - 'priority'.
    """
    posttweetset = models.ForeignKey(
        PostTweetSet, related_name='periodictweets')
    tweet = models.ForeignKey(Tweet)
    priority = models.IntegerField()

    def __unicode__(self):
        return '%s' % (self.tweet,)

    class Meta:
        unique_together = ('tweet', 'posttweetset',)
