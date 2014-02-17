from celery import task, Task, chain

import twitter

from .utils import get_api


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
    """
    Posts tweet with pk 'tweet_pk'. If everything is ok returns 'True',
    otherwise deletes tweet model and returns 'False'.
    """
    from .models import Tweet
    tweet_to_post = Tweet.objects.get(pk=tweet_pk)
    try:
        tweet.api.PostUpdate(tweet_to_post.status)
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
    """
    Gets next tweet from PostTweetSet with pk 'tweetset_pk' and if it exists
    tries to post it using 'tweet' task.
    """
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
    """
    Register PostTweetSet with pk 'tweetset_pk' in MQ using 'TaskScheduler'.
    """
    from .models import TaskScheduler
    task = TaskScheduler.create('tweets.tasks.post_next_tweet', period, every,
                                args="[" + '"%s"' % str(tweetset_pk) + "]")
    task.start()
