from datetime import datetime

from django.db import models
from django.db.models import signals

from djcelery.models import PeriodicTask, PeriodicTasks, IntervalSchedule

from .tasks import tweet, start_tweet_set


class TaskScheduler(PeriodicTask):

    class Meta:
        proxy = True

    @classmethod
    def create(cls, task_name, period, every, args="[]", kwargs="{}"):
        per_task_name = "%s_%s" % (task_name, datetime.now())
        interval, _ = IntervalSchedule.objects.get_or_create(
            period=period, every=every)
        ts = cls(name=per_task_name, task=task_name,
                 interval=interval, args=args, kwargs=kwargs, enabled=False)
        return ts

    def start(self):
        self.enabled = True
        self.save()

    def stop(self):
        self.enabled = False
        self.save()

    def terminate(self):
        self.stop()
        self.delete()

signals.pre_save.connect(PeriodicTasks.changed, sender=TaskScheduler)


class Tweet(models.Model):
    status = models.CharField(max_length=140)
    username = models.CharField(
        max_length=140, default='vladboyyko', editable=False)

    def __unicode__(self):
        return "'%s' by %s" % (self.status, self.username)


class PostTweetSet(models.Model):
    interval = models.ForeignKey(IntervalSchedule)
    description = models.CharField(max_length=200)
    start_time = models.DateTimeField()

    def next_tweet(self):
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


class TimedTweet(models.Model):
    tweet = models.ForeignKey(Tweet)
    post_time = models.DateTimeField()

    def __unicode__(self):
        return "Post '%s' at %s" % (self.tweet, self.post_time)

    def save(self, *args, **kwargs):
        super(TimedTweet, self).save(*args, **kwargs)
        tweet.apply_async(args=[self.tweet.pk], eta=self.post_time)


class PeriodicTweet(models.Model):
    tweetset = models.ForeignKey(PostTweetSet, related_name='tweets')
    tweet = models.ForeignKey(Tweet)
    priority = models.IntegerField()
    already_posted = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % (self.tweet,)
