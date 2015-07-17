from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property

import datetime
import dateutil.parser
import time


class Paste(models.Model):
    raw_paste = models.TextField()
    parsed = models.TextField()
    created = models.DateTimeField(editable=False)

    # taken from this discussion of object date stamps:
    # http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
    def save(self, *args, **kwargs):
        '''Set value of created field on first save() call.'''
        if not self.id:
            self.created = datetime.datetime.utcnow()
        return super(Paste, self).save(*args, **kwargs)


class EveUser(AbstractUser):
    '''Custom user class to work with django-social-auth'''

    @cached_property
    def _eve_auth(self):
        '''Shortcut to python-social-auth's EVE-related extra data for user.'''
        return self.social_auth.get(provider='eveonline').extra_data

    def _get_crest_tokens(self):
        '''Get tokens for authenticated CREST.'''
        expires_in = time.mktime(
            dateutil.parser.parse(
                self._eve_auth['expires']   # expiration time string
            ).timetuple()                   # expiration timestamp
        ) - time.time()                     # seconds until expiration
        return {
            'access_token': self._eve_auth['access_token'],
            'refresh_token': self._eve_auth['refresh_token'],
            'expires_in': expires_in
        }

    @property
    def character_id(self):
        '''Get CharacterID from authentification data.'''
        return self._eve_auth['id']

    def get_portrait_url(self, size=128):
        '''returns URL to character portrait from the Eve Image Server'''
        return 'https://image.eveonline.com/Character{0}_{1}.jpg'.format(
                self.character_id, size)
