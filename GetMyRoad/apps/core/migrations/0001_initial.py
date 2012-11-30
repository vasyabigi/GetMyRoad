# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('core_category', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('is_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Category'])

        # Adding model 'Place'
        db.create_table('core_place', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('checkins', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('likes', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('rank', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('pic', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('pic_small', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('price_range', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Place'])

        # Adding M2M table for field categories on 'Place'
        db.create_table('core_place_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('place', models.ForeignKey(orm['core.place'], null=False)),
            ('category', models.ForeignKey(orm['core.category'], null=False))
        ))
        db.create_unique('core_place_categories', ['place_id', 'category_id'])

        # Adding model 'Trip'
        db.create_table('core_trip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('core', ['Trip'])

        # Adding M2M table for field categories on 'Trip'
        db.create_table('core_trip_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trip', models.ForeignKey(orm['core.trip'], null=False)),
            ('category', models.ForeignKey(orm['core.category'], null=False))
        ))
        db.create_unique('core_trip_categories', ['trip_id', 'category_id'])

        # Adding model 'TripPoint'
        db.create_table('core_trippoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Category'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Place'])),
            ('arrive', self.gf('django.db.models.fields.DateTimeField')()),
            ('leave', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('core', ['TripPoint'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('core_category')

        # Deleting model 'Place'
        db.delete_table('core_place')

        # Removing M2M table for field categories on 'Place'
        db.delete_table('core_place_categories')

        # Deleting model 'Trip'
        db.delete_table('core_trip')

        # Removing M2M table for field categories on 'Trip'
        db.delete_table('core_trip_categories')

        # Deleting model 'TripPoint'
        db.delete_table('core_trippoint')


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