from rest_framework import serializers
from .models import WebPage, Link, Album, Track

class WebPageSerializer(serializers.ModelSerializer):
    links = serializers.HyperlinkedIdentityField('links', view_name='link-list')
    
    class Meta:
        model = WebPage
        fields = ('location', 'links', 'id')

class LinkSerializer(serializers.ModelSerializer):
	#page = WebPageSerializer()

	class Meta:
		model = Link
		order_by = 'url'

class AlbumSerializer(serializers.ModelSerializer):
	#tracks = serializers.RelatedField(many=True)

	class Meta:
		model = Album
		fields = ('album_name', 'artist', 'tracks',)