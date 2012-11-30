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
    trip = Trip.objects.get(name="test")

    places = trip.points.values('place__lat', 'place__lon').order_by('place__lon')

    # context = {
    #     'places': places,
    # }
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
