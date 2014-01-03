from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from .models import WebPage, Link
from .serializers import WebPageSerializer, LinkSerializer
from rest_framework import viewsets

from celery.result import AsyncResult

class WebPageViewSet(viewsets.ModelViewSet):
	queryset = WebPage.objects.all()
	serializer_class = WebPageSerializer

class LinkViewSet(viewsets.ModelViewSet):
	queryset = Link.objects.all()
	serializer_class = LinkSerializer

