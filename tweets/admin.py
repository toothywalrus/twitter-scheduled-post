from django.contrib import admin

from .models import Tweet, TimedTweet

import utils


class TweetAdmin(admin.ModelAdmin):
    list_display = ('status', 'created_on',)


class TimedTweetAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'post_time', 'already_posted',)

admin.site.register(Tweet, TweetAdmin)
admin.site.register(TimedTweet, TimedTweetAdmin)

for model in utils.get_info_models():
    try:
        admin.site.register(model)
    except Exception:
        pass
