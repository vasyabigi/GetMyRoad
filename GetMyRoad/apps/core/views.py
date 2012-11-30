from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Trip


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
    import ipdb; ipdb.set_trace()

    context = {
        'places': places
    }
    return Response(context)
