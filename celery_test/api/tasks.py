from celery import task, current_task
from celery.result import AsyncResult
from time import sleep
#from celery.decorators import task

import urllib2
from BeautifulSoup import BeautifulSoup as Soup

from .models import WebPage, Link

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

@task()
def scrap_page(page_pk):
	print "dfdf"
	webpage = WebPage.objects.get(pk=page_pk)
	page = urllib2.urlopen(webpage.location)
	html = page.read()
	webpage.html = html
	soup = Soup(html)
	validate = URLValidator()
	for a in soup.findAll('a'):
		try:
			validate(a['href'])
			link, created = Link.objects.get_or_create(page=webpage, url=a['href'])
			if not created:
				link.count += 1
				link.save()
		except ValidationError:
			pass
	webpage.save(populated=False)