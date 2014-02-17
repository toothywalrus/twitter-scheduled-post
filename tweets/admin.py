from django.contrib import admin

from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet


class TweetAdmin(admin.ModelAdmin):
    readonly_fields = ('username', )
    list_display = ('status', 'username', 'created_on',)


class TimedTweetAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'post_time', 'already_posted',)

admin.site.register(Tweet, TweetAdmin)
admin.site.register(TimedTweet, TimedTweetAdmin)
admin.site.register(PeriodicTweet)
admin.site.register(PostTweetSet)
