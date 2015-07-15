# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Paste.parsed'
        db.add_column(u'main_paste', 'parsed',
                      self.gf('django.db.models.fields.TextField')(default=-1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Paste.parsed'
        db.delete_column(u'main_paste', 'parsed')


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