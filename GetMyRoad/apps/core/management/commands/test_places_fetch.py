import logging

from django.core.management.base import BaseCommand

from core.models import Trip
from django.contrib.auth.models import User

logger = logging.getLogger("wheretogo.%s" % __name__)


class Command(BaseCommand):
    args = 'lat, lon, oauth_token'

    def handle(self, *args, **options):
        lat, lon, token = 37.75377496892, -122.42077080676, \
        	"AAACEdEose0cBAOLOdK4eZAxsHl3rGvtROrp2c42uoYsmXJN4BksjPDqD7Sc5KmSatpZCwm0igegdm3SfftgyxuIP4xbUi3KbDDurUnZAQZDZD"

        admin_user = User.objects.get(username='admin')
        trip = Trip(name="test", lat=float(lat), lon=float(lon), user=admin_user)
        trip.save()
        trip.fetch_places(token)
