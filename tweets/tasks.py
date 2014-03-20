from celery import task, Task, chain

import twitter

from .utils import get_api


# class BaseTwitterTask(Task):
#     abstract = True

#     _api = None

#     @property
#     def api(self):
#         if self._api is None:
#             self._api = get_api()
#         return self._api


# @task(base=BaseTwitterTask)
@task(throws=(twitter.TwitterError))
def tweet(tweet_pk, user_pk):
    """
    Posts tweet with pk 'tweet_pk'. If everything is ok returns 'True',
    otherwise deletes tweet model and returns 'False'.
    """
    from .models import Tweet, TwitterUser
    user = TwitterUser.objects.get(pk=user_pk)
    api = user.get_api()
    tweet_to_post = Tweet.objects.get(pk=tweet_pk)
    try:
        api.PostUpdate(tweet_to_post.status)
        return True
    except twitter.TwitterError, ex:
        raise ex


@task
def post_timed_tweet(ttweet_pk, user_pk):
    from .models import TimedTweet
    ttweet = TimedTweet.objects.get(pk=ttweet_pk)

    chain(tweet.s(ttweet.tweet.pk, user_pk),
          mark_posted.s(ttweet.pk, 'TimedTweet')).apply_async()


@task
def mark_posted(is_posted, pk, model_name):
    if is_posted:
        import models
        model = getattr(models, model_name)
        inst = model.objects.get(pk=pk)
        inst.already_posted = True
        inst.save(update_fields=['already_posted'])
        print 'mark posted'


@task
def post_next_tweet(tweetset_pk):
    """
    Gets next tweet from PostTweetSet with pk 'tweetset_pk' and if it exists
    tries to post it using 'tweet' task.
    """
    from .models import PostTweetSet
    try:
        tweetset = PostTweetSet.objects.get(pk=tweetset_pk)
        users = tweetset.users.all()
        print users
        next_tweet = tweetset.next_tweet()
        if next_tweet is not None:
            for user in users:
                chain(tweet.s(next_tweet.tweet.pk, user.pk), mark_posted.s(
                    next_tweet.pk, 'PeriodicTweet')).apply_async()
        else:
            print "nothing to post"
    except PostTweetSet.DoesNotExist:
        pass


@task
def start_tweet_set(ts_pk):
    from .models import TaskScheduler
    ts = TaskScheduler.objects.get(pk=ts_pk)
    ts.start()
