from rest_framework import serializers

from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet


class TimedTweetSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer(source='tweet')

    class Meta:
        model = TimedTweet


class PeriodicTweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = PeriodicTweet


class PostTweetSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostTweetSet
