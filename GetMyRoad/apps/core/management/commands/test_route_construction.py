import logging

from django.core.management.base import BaseCommand

from core.models import Trip
from django.contrib.auth.models import User

logger = logging.getLogger("wheretogo.%s" % __name__)


class Command(BaseCommand):
    args = 'lat, lon, oauth_token'

    def handle(self, *args, **options):
        lat, lon = 37.75377496892, -122.42077080676

        admin_user = User.objects.get(username='admin')
        Trip.objects.filter(name='test').delete()
        trip = Trip(name="test", lat=float(lat), lon=float(lon), user=admin_user)
        trip.save()
        trip.find_route(set([
        	273819889375819, 200600219953504, 192511100766680, 133436743388217,
        	209889829023118
        ]))
