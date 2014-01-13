from django.db import models


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
