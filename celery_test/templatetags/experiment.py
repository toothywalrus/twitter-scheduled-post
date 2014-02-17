from django import template

from tweets.models import Tweet

register = template.Library()


@register.inclusion_tag('etweets.html')
def show_tweets():
    tweets = Tweet.objects.all()
    return {'tweets': tweets}
