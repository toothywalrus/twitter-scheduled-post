from django.conf import settings

from celery import task, Task, chain

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
    from .models import Tweet
    tweet_to_post = Tweet.objects.get(pk=tweet_pk)
    try:
        tweet.api.PostUpdate(tweet_to_post.status)
        print tweet_to_post
        return True
    except twitter.TwitterError:
        print "error, this tweet will be deleted"
        tweet_to_post.delete()
    return False


@task
def mark_posted(is_posted, ptweet_pk):
    if is_posted:
        from .models import PeriodicTweet
        ptweet = PeriodicTweet.objects.get(pk=ptweet_pk)
        ptweet.already_posted = True
        ptweet.save()


@task
def post_next_tweet(tweetset_pk):
    from .models import PostTweetSet
    s = PostTweetSet.objects.get(pk=tweetset_pk)
    next_tweet = s.next_tweet()
    if next_tweet is not None:
        chain(tweet.s(next_tweet.tweet.pk),
              mark_posted.s(next_tweet.pk)).apply_async()
    else:
        print "nothing to post"


@task
def start_tweet_set(tweetset_pk, period, every):
    from .models import TaskScheduler
    task = TaskScheduler.create('tweets.tasks.post_next_tweet', period, every,
                                args="[" + '"%s"' % str(tweetset_pk) + "]")
    task.start()
