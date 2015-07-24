import datetime
from django.db import models


class Paste(models.Model):
    ep_id = models.IntegerField(primary_key=True)
    ep_link = models.URLField(null=True)
    ep_json = models.TextField(null=True)
    ep_kind = models.CharField(max_length=100, null=True)
    ep_market_id = models.IntegerField(null=True)
    ep_market_name = models.CharField(max_length=100, null=True)
    ep_totals_buy = models.FloatField(null=True)
    ep_totals_sell = models.FloatField(null=True)
    ep_totals_volume = models.BigIntegerField(null=True)
    character = models.ManyToManyField('main.Character')
    created = models.DateTimeField(editable=False, null=True)
    blueloot_value = models.FloatField(null=True)
    salvage_value = models.FloatField(null=True)

    def __unicode__(self):
        return 'Paste {}'.format(self.ep_id)


class Character(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
