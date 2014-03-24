from celery import task, chord

import twitter

import utils

# class BaseTwitterTask(Task):
#     abstract = True
#     _api = None
#     @property
#     def api(self):
#         if self._api is None:
#             self._api = get_api()
#         return self._api
# @task(base=BaseTwitterTask)


@task
def tweet(tweet_pk, user_pk):
    """
    Posts tweet with pk 'tweet_pk'. If everything is ok returns 'True',
    otherwise deletes tweet model and returns 'False'.
    """
    from .models import Tweet, TwitterUser
    user = TwitterUser.objects.get(pk=user_pk)
    api = user.get_api()
    tweet_to_post = Tweet.objects.get(pk=tweet_pk)
    if not utils.is_posted(tweet_pk, user_pk):
        try:
            api.PostUpdate(tweet_to_post.status)
            utils.mark_posted(tweet_pk, user_pk)
        except twitter.TwitterError:
            pass
    else:
        pass


@task
def mark_already_posted(model, pk):
    utils.set_already_posted(model, pk)


@task
def post_for_all_users(model, pk, users_qs):
    inst = model.objects.get(pk=pk)
    tweet_pk = inst.tweet.pk
    chord(tweet.si(tweet_pk, user.pk)
          for user in users_qs)(mark_already_posted.si(model, pk))


@task
def post_timed_tweet(timedtweet_pk):
    from .models import TimedTweet
    timedtweet = TimedTweet.objects.get(pk=timedtweet_pk)
    users = timedtweet.users.all()

    post_for_all_users(TimedTweet, timedtweet_pk, users)


@task
def post_next_tweet(tweetset_pk):
    """
    Gets next tweet from PostTweetSet with pk 'tweetset_pk' and if it exists
    tries to post it using 'tweet' task.
    """
    from .models import PostTweetSet, PeriodicTweet
    try:
        tweetset = PostTweetSet.objects.get(pk=tweetset_pk)
        users = tweetset.users.all()
        next_tweet = tweetset.next_periodic_tweet()
        if next_tweet is not None:
            post_for_all_users(PeriodicTweet, next_tweet.pk, users)
        else:
            print "nothing to post"
    except PostTweetSet.DoesNotExist:
        pass


@task
def start_tweet_set(ts_pk):
    from .models import TaskScheduler
    ts = TaskScheduler.objects.get(pk=ts_pk)
    ts.start()
