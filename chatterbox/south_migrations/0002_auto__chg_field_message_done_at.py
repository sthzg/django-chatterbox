# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Message.done_at'
        db.alter_column(u'chatterbox_message', 'done_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Message.done_at'
        raise RuntimeError("Cannot reverse this migration. 'Message.done_at' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Message.done_at'
        db.alter_column(u'chatterbox_message', 'done_at', self.gf('django.db.models.fields.DateTimeField')())

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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'originator': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10', 'max_length': '2'}),
            'scheduled_for': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'should_cancel': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['chatterbox']