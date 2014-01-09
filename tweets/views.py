from django.shortcuts import render_to_response
from django.template import RequestContext

def MainHomePage(request):
	context = {'tweets': getTweets()}
	return render_to_response('index.html', context, context_instance=RequestContext(request))

def getTweets():
	tweets = []
	try:
		import twitter
		api = twitter.Api()
		latest = api.GetUserTimeline('HackedExistance')
		for tweet in latest:
			status = tweet.text
			tweet_date = tweet.relative_created_at
			tweets.append({'status': status, 'date': tweet_date})
	except:
		tweets.append({'status': 'Follow us @HackedExistance', 'date': 'about 10 min ago'})
	return {'tweets': tweets}