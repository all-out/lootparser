# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Paste.created'
        db.alter_column(u'main_paste', 'created', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'Paste.created'
        db.alter_column(u'main_paste', 'created', self.gf('django.db.models.fields.DateField')())

    models = {
        u'main.paste': {
            'Meta': {'object_name': 'Paste'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_paste': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['main']