import logging
import urllib
import urllib2
import json
import math

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


logger = logging.getLogger("gmr.%s" % __name__)


class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField('Name', max_length=250)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

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
    lat = models.DecimalField('Lat', decimal_places=15, max_digits=50)
    lon = models.DecimalField('Lng', decimal_places=15, max_digits=50)
    hours = models.TextField('Hours', blank=True, null=True)

    class Meta:
        ordering = ['rank']

    def __unicode__(self):
        return self.name

    def get_time_to_get(self, lat, lon, reverse=False):
        # TODO: Replace with google api calls
        lat1, lon1 = float(self.lat), float(self.lon)
        lat2, lon2 = float(lat), float(lon)
        radius = 6371.0  # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c

        res = timedelta(seconds=int((d / 40.) * 3600.))
        return res

    def get_avg_spend_time(self, current_time=None):
        '''avg time people spends in this place'''

        return timedelta(seconds=3600*1.5)

    def does_work(self, time):
        from dateutil import parser
        try:
            data = json.loads(self.hours)
        except:
            return True
        else:
            if data:
                wd = time.strftime('%a').lower()
                try:
                    open_from_1 = parser.parse(
                      data.get("%s_1_open" % wd, None)
                    )
                except AttributeError:
                    return True
                try:
                    open_from_2 = parser.parse(
                      data.get("%s_2_open" % wd, None)
                    )
                except AttributeError:
                    open_from_2 = None
                try:
                    close_from_1 = parser.parse(
                      data.get("%s_1_close" % wd, None)
                    )
                except AttributeError:
                    return True
                try:
                    close_from_2 = parser.parse(
                      data.get("%s_2_close" % wd, None)
                    )
                except AttributeError:
                    close_from_2 = None
                try:
                    return (
                        open_from_1 <= time + self.get_avg_spend_time() <= close_from_1
                    ) or (
                        open_from_2 and close_from_2 and \
                        open_from_2 <= time + self.get_avg_spend_time() <= close_from_2
                        
                    )
                except TypeError:
                    return True
        return True


class TripManager(models.Manager):
    pass


class Trip(models.Model):
    name = models.CharField('Trip Name', max_length=250)
    user = models.ForeignKey(User, related_name="trips")
    categories = models.ManyToManyField(Category)
    lat = models.DecimalField('Lat', decimal_places=15, max_digits=50)
    lon = models.DecimalField('Lon', decimal_places=15, max_digits=50)
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(
        default=lambda: datetime.now() + timedelta(seconds=3600*8)
    )
    places = models.ManyToManyField(
        'Place', blank=True, null=True, related_name='trips'
    )
    categories = models.ManyToManyField(
        'Category', blank=True, null=True, related_name='trips'
    )
    estimated_time = models.CharField(
        blank=True, null=True, max_length=50
    )

    RADIUS = 50000

    objects = TripManager()

    def __unicode__(self):
        return self.name

    def fetch_places(self):
        '''fetch places from facebook from give circle'''

        social_user = self.user.social_auth.get()

        url = 'https://graph.facebook.com/search?%s' % urllib.urlencode({
            'fields': 'id',
            'type': 'place',
            'center': "%f,%f" % (self.lat, self.lon),
            'distance': "%.0f" % self.RADIUS,
            'access_token': social_user.extra_data['access_token'],
            'limit': 500
        })

        while url:
            logger.debug(u'Trying to get places list from Facebook with url: %s' % url)
            response = urllib2.urlopen(url)
            data = json.loads(response.read())
            url = data.get('paging', {}).get('next', False)
            print url
            place_ids = [item['id'] for item in data['data']]
            if not place_ids:
                break
            logger.debug(u'Fetched places ids: %s' % place_ids)

            path = 'https://graph.facebook.com/fql?%s' % urllib.urlencode({
                'q': '''
                    SELECT name, page_id, fan_count, checkins,
                        location, pic, pic_small, price_range,
                        phone, categories, hours
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
                        lon=place_data['location']['longitude'],
                        hours=json.dumps(place_data['hours'])
                    )
                    for cat_data in place_data['categories']:
                        cat, c = Category.objects.get_or_create(
                            id=cat_data['id'],
                            name=cat_data['name']
                        )
                        place.categories.add(cat)
                for cat_data in place_data['categories']:
                    self.categories.add(cat_data['id'])
                self.places.add(place)

    def find_route(self, categories):
        from core.finder import find

        # deleting old trip point, if exist
        self.points.all().delete()
        places = {}
        for cat in categories:
            # TODO: add distance filtering
            places[cat] = self.places.filter(categories=cat) \
                .order_by('-rank')[:15]
        route, time = find(
            self.lat, self.lon, categories, places,
            self.start, self.end
        )
        self.estimated_time = unicode(time - self.start)
        self.save()
        for point in route:
            TripPoint.objects.create(
                trip=self,
                place=point.place,
                arrive=point.time,
                leave=point.time + point.place.get_avg_spend_time(
                    point.time
                )
            )


class TripPoint(models.Model):
    trip = models.ForeignKey(Trip, related_name="points")
    place = models.ForeignKey(Place, related_name="points")
    arrive = models.DateTimeField(blank=True, null=True)
    leave = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['arrive']

    def __unicode__(self):
        return u'%s for %s' % (self.place, self.trip)
