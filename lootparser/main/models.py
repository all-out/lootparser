import datetime
from django.db import models


class Paste(models.Model):
    raw_paste = models.TextField()
    created = models.DateTimeField(editable=False)

    # taken from this discussion of object date stamps:
    # http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
    def save(self, *args, **kwargs):
        '''Set value of created field on first save() call.'''
        if not self.id:
            self.created = datetime.datetime.utcnow()
        return super(Paste, self).save(*args, **kwargs)
