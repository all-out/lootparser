from django.db import models


class Paste(models.Model):
    contents = models.TextField(null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return creation_date
