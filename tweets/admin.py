from django.contrib import admin

from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet,\
    TwitterUser, Interval


class TweetAdmin(admin.ModelAdmin):
    list_display = ('status', 'created_on',)


class TimedTweetAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'post_time', 'already_posted',)

admin.site.register(Tweet, TweetAdmin)
admin.site.register(TimedTweet, TimedTweetAdmin)
admin.site.register(PeriodicTweet)
admin.site.register(PostTweetSet)
admin.site.register(TwitterUser)
admin.site.register(Interval)
