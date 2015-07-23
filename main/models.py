import datetime
from django.db import models


class Paste(models.Model):
    ep_id = models.IntegerField(primary_key=True)
    ep_link = models.URLField()
    ep_json = models.TextField()
    ep_kind = models.CharField(max_length=100)
    ep_market_id = models.IntegerField()
    ep_market_name = models.CharField(max_length=100)
    ep_totals_buy = models.BigIntegerField()
    ep_totals_sell = models.BigIntegerField()
    ep_totals_volume = models.BigIntegerField()
    character = models.ManyToManyField('main.Character')
    created = models.DateTimeField(editable=False)

    # taken from this discussion of object date stamps:
    # http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
    def save(self, *args, **kwargs):
        '''Set value of created field on first save() call.'''
        if not self.id:
            self.created = datetime.datetime.utcnow()
        return super(Paste, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Paste {:07d}'.format(self.id)


class Character(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
