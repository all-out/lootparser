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
    ep_totals_volume = models.FloatField(null=True)
    character = models.ManyToManyField('main.Character', blank=True)
    created = models.DateTimeField(editable=False, null=True)
    blueloot_value = models.FloatField(null=True)
    salvage_value = models.FloatField(null=True)
    total_value = models.FloatField(null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    op = models.ForeignKey('main.Op', null=True, blank=True)
    tax = models.ForeignKey('main.Tax', default=1)

    def __unicode__(self):
        paste_string = 'Paste: '
        if self.name is not None and self.name != '':
            return self.name
        else:
            return str(self.ep_id)


class Op(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        if self.name is not None and self.name != '':
            return self.name
        else:
            return str(self.id)


class Character(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Taxes'
