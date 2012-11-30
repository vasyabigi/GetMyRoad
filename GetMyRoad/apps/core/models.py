import logging
import urllib
import urllib2
import json

from django.db import models


class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField('Name', max_length=250)
    is_main = models.BooleanField(default=False)

    @property
    def place_count(self):
        return  self.places.count()


class Place(models.Model):
    id = models.BigIntegerField(primary_key=True)
    categories = models.ManyToManyField(Category, related_name='places')
    name = models.CharField('Name', max_length=250)
    checkins = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    rank = models.BigIntegerField(default=0)
    pic = models.CharField(blank=True, null=True, max_length=250)
    pic_small = models.CharField(blank=True, null=True, max_length=250)
    price_range = models.CharField(blank=True, null=True, max_length=250)
    phone = models.CharField(blank=True, null=True, max_length=250)

    class Meta:
        ordering = ['rank']


class TripManager(models.Manager):
    pass


class Trip(models.Model):
    name = models.CharField('Trip Name', max_length=250)
    categories = models.ManyToManyField(Category)

    objects = TripManager()

    def fetch_places(self, lat, lon, radius, oauth_token):
        '''fetch places from facebook from give circle'''

        path = 'https://graph.facebook.com/search?fields=id%s' % urllib.urlencode({
            'type': 'place',
            'center': "%f,%f" % (lat, lon),
            'distance': "%.0f" % radius,
            'access_token': oauth_token,
            'limit': 500
        })
        logger.debug(u'Trying to get places list from Facebook with url: %s' % path)
        response = urllib2.urlopen(path)
        data = json.loads(response.read())
        # TODO retrieve info from next pages if numbers less than 500
        results = []
        place_ids = [item['id'] for item in data['data']]
        logger.debug(u'Fetched places ids: %s' % place_ids)

        path = 'https://graph.facebook.com/search?fields=id%s' % urllib.urlencode({
            'type': 'place',
            'center': "%f,%f" % (lat, lon),
            'distance': "%.0f" % radius,
            'access_token': oauth_token,
            'limit': 500
        })
        logger.debug(u'Trying to get places list from Facebook with url: %s' % path)
        response = urllib2.urlopen(path)


class TripPoint(models.Model):
    category = models.ForeignKey(Category)
    place = models.ForeignKey(Place)
    arrive = models.DateTimeField()
    leave = models.DateTimeField()
    