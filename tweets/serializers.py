from rest_framework import serializers

from djcelery.models import IntervalSchedule

from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet


class IntervalSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntervalSchedule
        fields = ('every', 'period',)


class TimedTweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimedTweet
        fields = ('already_posted', 'post_time', )


class TweetSerializer(serializers.ModelSerializer):
    timedtweets = TimedTweetSerializer(many=True)

    class Meta:
        model = Tweet
        fields = ('id', 'status', 'username', 'created_on', 'timedtweets', )


class PeriodicTweetSerializer(serializers.ModelSerializer):

    class TweetSerializer(serializers.ModelSerializer):

        class Meta:
            model = Tweet
            fields = ('status', 'username',)

    class Meta:
        model = PeriodicTweet
        fields = ('already_posted', 'posted_on', 'priority', 'tweet', )

    tweet = TweetSerializer(source='tweet')


class PostTweetSetSerializer(serializers.ModelSerializer):
    interval = IntervalSerializer(source='interval')
    periodictweets = PeriodicTweetSerializer(source='tweets', many=True)

    class Meta:
        model = PostTweetSet
