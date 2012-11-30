from cloudmade import routing
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Trip

router = routing.Router("f3f25538fbae4777b3e2c8ff3f6d53f5", "navigation.cloudmade.com")


def home(request):
    return render(request, 'core/home.html')


def logout(request):
    auth_logout(request)
    return redirect('home')


@api_view(['POST'])
def find_places(request):
    places = None

    # request.POST['lat'], request.POST['lng']

    # Place for Anton job
    if request.user.is_authenticated():
        trip, created = Trip.objects.get_or_create(
            user=request.user,
            lat=float(request.POST['lat']),
            lon=float(request.POST['lng'])
        )
        trip.fetch_places()
        trip.find_route(set([
            273819889375819, 200600219953504, 192511100766680, 133436743388217,
            209889829023118
        ]))

    places = trip.points.values('place__lat', 'place__lon')

    return Response(places)


@api_view(['POST'])
def build_road(request):
    start_lat = float(request.POST['start_lat'])
    start_lng = float(request.POST['start_lng'])
    end_lat = float(request.POST['end_lat'])
    end_lng = float(request.POST['end_lng'])
    query = routing.Query([start_lat, start_lng], [end_lat, end_lng])
    result = router.route(query)
    return Response(result)
