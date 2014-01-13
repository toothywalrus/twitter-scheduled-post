from rest_framework import serializers
from .models import WebPage, Link


class WebPageSerializer(serializers.ModelSerializer):
    links = serializers.HyperlinkedIdentityField(
        'links', view_name='link-list')

    class Meta:
        model = WebPage
        fields = ('location', 'links', 'id')


class LinkSerializer(serializers.ModelSerializer):
        #page = WebPageSerializer()

    class Meta:
        model = Link
        order_by = 'url'
