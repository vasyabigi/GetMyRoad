import logging

from django.core.management.base import BaseCommand

from core.models import Trip
from django.contrib.auth.models import User

logger = logging.getLogger("wheretogo.%s" % __name__)


class Command(BaseCommand):
    args = 'lat, lon, oauth_token'

    def handle(self, *args, **options):
        lat, lon, token = 37.76745803822967, -122.43988037109374, \
            "AAACEdEose0cBAMvhh6NH5ZAxaeuRsZB7TUQ0HXTZAkXOdr5JrlftC91WS0UqEm581S3XgDuaiIjiaVi9cO5QNWrbuDhxWQlY2yhSXG18wZDZD"

        admin_user = User.objects.get(username='admin')
        trip = Trip(name="test", lat=float(lat), lon=float(lon), user=admin_user)
        trip.save()
        trip.fetch_places()
        trip.find_route(set([
        	273819889375819, 200600219953504, 192511100766680, 133436743388217,
        	209889829023118
        ]))
