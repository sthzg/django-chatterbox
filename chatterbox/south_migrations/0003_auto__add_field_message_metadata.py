# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Message.metadata'
        db.add_column(u'chatterbox_message', 'metadata',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Message.metadata'
        db.delete_column(u'chatterbox_message', 'metadata')


    models = {
        u'chatterbox.message': {
            'Meta': {'object_name': 'Message'},
            'cancel_reason': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '500', 'null': 'True'}),
            'channel': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'}),
            'channel_data': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'content': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'done_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'metadata': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'originator': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10', 'max_length': '2'}),
            'scheduled_for': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'should_cancel': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['chatterbox']