# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WebPage'
        db.create_table(u'api_webpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'api', ['WebPage'])

        # Adding model 'Link'
        db.create_table(u'api_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.WebPage'])),
        ))
        db.send_create_signal(u'api', ['Link'])


    def backwards(self, orm):
        # Deleting model 'WebPage'
        db.delete_table(u'api_webpage')

        # Deleting model 'Link'
        db.delete_table(u'api_link')


    models = {
        u'api.link': {
            'Meta': {'object_name': 'Link'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.WebPage']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'api.webpage': {
            'Meta': {'object_name': 'WebPage'},
            'html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['api']