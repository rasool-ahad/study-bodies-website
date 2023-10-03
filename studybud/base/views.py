from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    query = Room.objects.all()
    return render(request, "base/home.html", context={"rooms": query})

def room(request, id):
    room = Room.objects.get(pk=id)
    return render(request, "base/room.html", context={"room":room})
