import logging

from django.core.management.base import BaseCommand

from core.models import Trip
from django.contrib.auth.models import User

logger = logging.getLogger("wheretogo.%s" % __name__)


class Command(BaseCommand):
    args = 'lat, lon, oauth_token'

    def handle(self, *args, **options):
        lat, lon, token = 37.76745803822967, -122.43988037109374, \
            "AAACEdEose0cBACcx0R9oW2pCLxpTjJFAJFhnGJu8ZBogYY2BkZCdNnJu2TVYlJijY24aAm175wvGaZCbRjATlYe2uDVmsJElYUBeTRE5QZDZD"

        admin_user = User.objects.get(username='vasyabigi')
        trip = Trip(name="test", lat=float(lat), lon=float(lon), user=admin_user)
        trip.save()
        trip.fetch_places(token)
