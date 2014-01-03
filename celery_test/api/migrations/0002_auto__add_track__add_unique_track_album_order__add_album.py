# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Track'
        db.create_table(u'api_track', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tracks', to=orm['api.Album'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'api', ['Track'])

        # Adding unique constraint on 'Track', fields ['album', 'order']
        db.create_unique(u'api_track', ['album_id', 'order'])

        # Adding model 'Album'
        db.create_table(u'api_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'api', ['Album'])


    def backwards(self, orm):
        # Removing unique constraint on 'Track', fields ['album', 'order']
        db.delete_unique(u'api_track', ['album_id', 'order'])

        # Deleting model 'Track'
        db.delete_table(u'api_track')

        # Deleting model 'Album'
        db.delete_table(u'api_album')


    models = {
        u'api.album': {
            'Meta': {'object_name': 'Album'},
            'album_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'api.link': {
            'Meta': {'object_name': 'Link'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': u"orm['api.WebPage']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'api.track': {
            'Meta': {'unique_together': "(('album', 'order'),)", 'object_name': 'Track'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracks'", 'to': u"orm['api.Album']"}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'api.webpage': {
            'Meta': {'object_name': 'WebPage'},
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['api']