from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    return render(request, 'core/home.html')


def logout(request):
    auth_logout(request)
    return redirect('home')


@api_view(['GET'])
def find_places(request):
    places = None

    # Place for Anton job

    context = {
        'places': places
    }
    return Response(context)
