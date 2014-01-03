from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class WebPage(models.Model):
	html = models.TextField(blank=True, editable=False)
	location = models.URLField()

	def __unicode__(self):
		return '%s' % self.location

	def save(self, populated=True, *args, **kwargs):
		super(WebPage, self).save(*args, **kwargs)
		if populated:
			from .tasks import scrap_page
			scrap_page.delay(self.pk)


class Link(models.Model):
	url = models.URLField()
	count = models.IntegerField(default=1)
	page = models.ForeignKey('WebPage', related_name='links')

class Album(models.Model):
	album_name = models.CharField(max_length=100)
	artist = models.CharField(max_length=100)

class Track(models.Model):
	album = models.ForeignKey(Album, related_name='tracks')
	order = models.IntegerField()
	title = models.CharField(max_length=100)
	duration = models.IntegerField()

	class Meta:
		unique_together = ('album', 'order')
		#ordered = 'order'

	def __unicode__(self):
		return '%d: %s' % (self.order, self.title)