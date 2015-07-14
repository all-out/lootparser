# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Paste.raw_paste'
        db.add_column(u'main_paste', 'raw_paste',
                      self.gf('django.db.models.fields.TextField')(default=-1),
                      keep_default=False)

        # Adding field 'Paste.created'
        db.add_column(u'main_paste', 'created',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2015, 7, 14, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Paste.raw_paste'
        db.delete_column(u'main_paste', 'raw_paste')

        # Deleting field 'Paste.created'
        db.delete_column(u'main_paste', 'created')


    models = {
        u'main.paste': {
            'Meta': {'object_name': 'Paste'},
            'created': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_paste': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['main']