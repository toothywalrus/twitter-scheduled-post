from django.contrib.auth import get_user_model

from rest_framework import serializers

from djcelery.models import IntervalSchedule

from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet


class IntervalSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntervalSchedule
        fields = ('every', 'period',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', )


class TimedTweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimedTweet
        fields = ('already_posted', 'post_time', )


class TweetSerializer(serializers.ModelSerializer):
    timedtweets = TimedTweetSerializer(many=True)
    user = UserSerializer(source='user')

    class Meta:
        model = Tweet
        fields = ('id', 'status', 'user', 'created_on', 'timedtweets', )


class PeriodicTweetSerializer(serializers.ModelSerializer):

    class TweetSerializer(serializers.ModelSerializer):

        class Meta:
            model = Tweet
            fields = ('status', 'user',)

    class Meta:
        model = PeriodicTweet
        fields = ('already_posted', 'posted_on', 'priority', 'tweet', )

    tweet = TweetSerializer(source='tweet')


class PostTweetSetSerializer(serializers.ModelSerializer):
    interval = IntervalSerializer(source='interval')
    periodictweets = PeriodicTweetSerializer(source='tweets', many=True)

    class Meta:
        model = PostTweetSet
