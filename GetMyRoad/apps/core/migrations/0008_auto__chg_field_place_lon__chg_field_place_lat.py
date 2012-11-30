# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Place.lon'
        db.alter_column('core_place', 'lon', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=15))

        # Changing field 'Place.lat'
        db.alter_column('core_place', 'lat', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=15))

    def backwards(self, orm):

        # Changing field 'Place.lon'
        db.alter_column('core_place', 'lon', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Place.lat'
        db.alter_column('core_place', 'lat', self.gf('django.db.models.fields.FloatField')())

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '15'}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '15'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trips'", 'to': "orm['auth.User']"})
        },
        'core.trippoint': {
            'Meta': {'ordering': "['arrive']", 'object_name': 'TripPoint'},
            'arrive': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points'", 'to': "orm['core.Place']"}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points'", 'to': "orm['core.Trip']"})
        }
    }

    complete_apps = ['core']