# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Paste'
        db.create_table(u'main_paste', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('raw_paste', self.gf('django.db.models.fields.TextField')()),
            ('parsed', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'main', ['Paste'])


    def backwards(self, orm):
        # Deleting model 'Paste'
        db.delete_table(u'main_paste')


    models = {
        u'main.paste': {
            'Meta': {'object_name': 'Paste'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parsed': ('django.db.models.fields.TextField', [], {}),
            'raw_paste': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['main']