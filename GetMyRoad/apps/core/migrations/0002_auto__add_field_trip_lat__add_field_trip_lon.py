# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Trip.lat'
        db.add_column('core_trip', 'lat',
                      self.gf('django.db.models.fields.FloatField')(default=1),
                      keep_default=False)

        # Adding field 'Trip.lon'
        db.add_column('core_trip', 'lon',
                      self.gf('django.db.models.fields.FloatField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Trip.lat'
        db.delete_column('core_trip', 'lat')

        # Deleting field 'Trip.lon'
        db.delete_column('core_trip', 'lon')


    models = {
        'core.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'is_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'core.place': {
            'Meta': {'ordering': "['rank']", 'object_name': 'Place'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'places'", 'symmetrical': 'False', 'to': "orm['core.Category']"}),
            'checkins': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pic': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pic_small': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'price_range': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'core.trip': {
            'Meta': {'object_name': 'Trip'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Category']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'core.trippoint': {
            'Meta': {'object_name': 'TripPoint'},
            'arrive': ('django.db.models.fields.DateTimeField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave': ('django.db.models.fields.DateTimeField', [], {}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Place']"})
        }
    }

    complete_apps = ['core']