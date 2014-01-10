from django.conf import settings

from celery import task, Task

import twitter


def get_api(consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET):
    api = twitter.Api(
        consumer_key, consumer_secret, access_token_key, access_token_secret)
    return api


class BaseTwitterTask(Task):
    abstract = True

    _api = None

    @property
    def api(self):
        if self._api is None:
            self._api = get_api()
        return self._api


@task(base=BaseTwitterTask)
def tweet(tweet_pk):
    from .models import PeriodicTweet
    tweet_to_post = PeriodicTweet.objects.get(pk=tweet_pk)
    try:
        tweet.api.PostUpdate(tweet_to_post.tweet.status)
        tweet_to_post.already_posted = True
        tweet_to_post.save()
    except twitter.TwitterError:
        print "error, this tweet will be deleted"
        tweet_to_post.delete()


@task
def post_next_tweet(tweetset_pk):
    from .models import PostTweetSet
    s = PostTweetSet.objects.get(pk=tweetset_pk)
    next_tweet = s.next_tweet()
    if next_tweet is not None:
        tweet.delay(next_tweet.pk)
    else:
        print "nothing to post"


@task
def start_tweet_set(tweetset_pk, period, every):
    from .models import TaskScheduler
    task = TaskScheduler.create('tweets.tasks.post_next_tweet', period, every,
                                args="[" + '"%s"' % str(tweetset_pk) + "]")
    task.start()
