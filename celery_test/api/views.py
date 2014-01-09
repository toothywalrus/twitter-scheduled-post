from rest_framework import viewsets

from .models import WebPage, Link
from .serializers import WebPageSerializer, LinkSerializer


class WebPageViewSet(viewsets.ModelViewSet):
    queryset = WebPage.objects.all()
    serializer_class = WebPageSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
