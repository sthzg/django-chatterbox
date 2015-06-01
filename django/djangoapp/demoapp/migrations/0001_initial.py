# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Somemodel'
        db.create_table(u'demoapp_somemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'demoapp', ['Somemodel'])


    def backwards(self, orm):
        # Deleting model 'Somemodel'
        db.delete_table(u'demoapp_somemodel')


    models = {
        u'demoapp.somemodel': {
            'Meta': {'object_name': 'Somemodel'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['demoapp']