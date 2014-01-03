from django.contrib import admin

from .models import WebPage, Link

class WebPageAdmin(admin.ModelAdmin):
	readonly_fields = ('html', )

admin.site.register(WebPage, WebPageAdmin)
admin.site.register(Link)