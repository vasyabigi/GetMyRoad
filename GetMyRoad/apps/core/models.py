import logging
import urllib
import urllib2
import json
import math

from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


logger = logging.getLogger("gmr.%s" % __name__)


class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField('Name', max_length=250)
    is_main = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def place_count(self):
        return self.places.count()


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
    lat = models.FloatField('Lat')
    lon = models.FloatField('Lng')

    class Meta:
        ordering = ['rank']

    def __unicode__(self):
        return self.name

    def get_time_to_get(self, lat, lon):
        # TODO: Replace with google api calls
        lat1, lon1 = self.lat, self.lon
        lat2, lon2 = lat, lon
        radius = 6371 # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c

        return d / 40

class TripManager(models.Manager):
    pass


class Trip(models.Model):
    name = models.CharField('Trip Name', max_length=250)
    user = models.ForeignKey(User, related_name="trips")
    categories = models.ManyToManyField(Category)
    lat = models.FloatField('Lat')
    lon = models.FloatField('Lng')

    RADIUS = 50000

    objects = TripManager()

    def __unicode__(self):
        return self.name

    def fetch_places(self, oauth_token):
        '''fetch places from facebook from give circle'''

        path = 'https://graph.facebook.com/search?%s' % urllib.urlencode({
            'fields': 'id',
            'type': 'place',
            'center': "%f,%f" % (self.lat, self.lon),
            'distance': "%.0f" % self.RADIUS,
            'access_token': oauth_token,
            'limit': 500
        })
        logger.debug(u'Trying to get places list from Facebook with url: %s' % path)
        response = urllib2.urlopen(path)
        data = json.loads(response.read())
        logger.debug('Received data: %s' % data)
        place_ids = [item['id'] for item in data['data']]
        while data.get('paging', {}).get('next', None):
            next_page_url = data['paging']['next']
            response = urllib2.urlopen(next_page_url)
            data = json.loads(response.read())
            for item in data['data']:
                place_ids.append(item['id'])
        logger.debug(u'Fetched places ids: %s' % place_ids)

        path = 'https://graph.facebook.com/fql?%s' % urllib.urlencode({
            'q': '''
                SELECT name, page_id, fan_count, checkins,
                    location, pic, pic_small, price_range,
                    phone, categories
                FROM page
                WHERE page_id IN (%s)''' % ', '.join(place_ids)
        })
        logger.debug(u'Trying to get datailed places list from Facebook with url: %s' % path)
        response = urllib2.urlopen(path)
        data = json.loads(response.read())
        logger.debug('Received data: %s' % data)
        for place_data in data['data']:
            try:
                place = Place.objects.get(id=place_data['page_id'])
            except Place.DoesNotExist:
                place = Place.objects.create(
                    id=place_data['page_id'],
                    name=place_data['name'],
                    checkins=place_data['checkins'],
                    likes=place_data['fan_count'],
                    # TODO: convert tot more cool formula
                    rank=place_data['fan_count'] * 2 + place_data['checkins'],
                    pic=place_data['pic'],
                    pic_small=place_data['pic_small'],
                    price_range=place_data['price_range'],
                    phone=place_data['phone'],
                    lat=place_data['location']['latitude'],
                    lon=place_data['location']['longitude']
                )
                for cat_data in place_data['categories']:
                    cat, c = Category.objects.get_or_create(
                        id=cat_data['id'],
                        name=cat_data['name']
                    )
                    place.categories.add(cat)

    def find_route(self, categories):
        from core.finder import find
        places = {}
        for cat in categories:
            # TODO: add distance filtering
            places[cat] = Place.objects.filter(categories=cat) \
                .order_by('-rank')[:10]
        route = find(
            self.lat, self.lon, categories, places,
            timedelta(seconds=3600)
        )
        import ipdb; ipdb.set_trace()

class TripPoint(models.Model):
    trip = models.ForeignKey(Trip, related_name="points")
    place = models.ForeignKey(Place, related_name="points")
    arrive = models.DateTimeField(blank=True, null=True)
    leave = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s for %s' % (self.place, self.trip)
