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
    parent = serializers.PrimaryKeyRelatedField(source='tweet', read_only=True)

    class Meta:
        model = TimedTweet
        fields = ('id', 'already_posted', 'post_time', 'parent')


class TweetSerializer(serializers.ModelSerializer):
    timedtweets = TimedTweetSerializer(many=True)
    user = UserSerializer(source='user')

    class Meta:
        model = Tweet
        fields = ('id', 'status', 'user', 'created_on', 'timedtweets', )


class PeriodicTweetSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        source='tweetset', read_only=True)

    class TweetSerializer(serializers.ModelSerializer):

        class Meta:
            model = Tweet
            fields = ('status', 'user',)

    class Meta:
        model = PeriodicTweet
        fields = ('id', 'already_posted',
                  'posted_on', 'priority', 'tweet', 'parent')

    tweet = TweetSerializer(source='tweet')


class PostTweetSetSerializer(serializers.ModelSerializer):
    interval = IntervalSerializer(source='interval')
    periodictweets = PeriodicTweetSerializer(source='tweets', many=True)

    class Meta:
        model = PostTweetSet
