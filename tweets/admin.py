from django.contrib import admin

from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet


class TweetAdmin(admin.ModelAdmin):
    readonly_fields = ('username', )

admin.site.register(Tweet, TweetAdmin)
admin.site.register(TimedTweet)
admin.site.register(PeriodicTweet)
admin.site.register(PostTweetSet)
