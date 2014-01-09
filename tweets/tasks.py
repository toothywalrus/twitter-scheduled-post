from celery.task import periodic_task, PeriodicTask, Task
from celery import task
from datetime import timedelta
from celery.registry import tasks
# from .models import Period, PeriodTweet, TimeTweet
import twitter
from django.conf import settings

#api = settings.TWITTER_API
api = None

@task
def tweet(tweet_pk):
	from .models import Tweet
	tweet = Tweet.objects.get(pk=tweet_pk)
	tweet.already_posted = True
	api.PostUpdate(tweet.status)
	tweet.save()

@task
def post_next_tweet(tweetset_pk):
	from .models import PostTweetSet
	s = PostTweetSet.objects.get(pk=tweetset_pk)
	next_tweet = s.next_tweet()
	if next_tweet:
		tweet.delay(next_tweet.pk)
	else:
		print "nothing to post"

@task
def start_tweet_set(tweetset_pk, period, every):
	from .models import TaskScheduler
	task = TaskScheduler.create('tweets.tasks.post_next_tweet', period, every, args="[" + '"%s"' % str(tweetset_pk) + "]")
	task.start()
	print task.enabled