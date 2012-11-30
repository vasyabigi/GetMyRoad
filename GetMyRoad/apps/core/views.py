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
def select_categories(request):
    # request.POST['lat'], request.POST['lng']

    # Place for Anton job
    if request.user.is_authenticated():
        trip = Trip.objects.create(
            user=request.user,
            lat=float(request.POST['lat']),
            lon=float(request.POST['lng'])
        )
        trip.fetch_places()
    return Response({
        'trip_id': trip.id,
        'categories': [
            cat for cat in trip.categories.values('id', 'name') \
            if trip.place_count > 2
        ]
    })


@api_view(['POST'])
def find_places(request):
    places = None

    # Place for Anton job
    if request.user.is_authenticated():
        trip, created = Trip.objects.get_or_create(
            user=request.user,
            id=float(request.POST['id']),
        )
        trip.find_route(set([int(el) for el in request.POST.getlist('categories[]')]))

        places = trip.points.values('place__lat', 'place__lon', 'place__name', 'place__id')
    else:
        places = []
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
