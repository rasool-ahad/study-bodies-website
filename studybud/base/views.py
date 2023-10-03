from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import RoomForm
from django.db.models import Q
# Create your views here.


def home(request):
    search = request.GET.get("q", "")
    rooms = Room.objects.filter(Q(topic__name__icontains=search) |
                                Q(host__username__icontains=search) |
                                Q(description__icontains=search))
    topic = Topic.objects.all()
    count = rooms.count()

    context = {"rooms": rooms, "topics": topic, "count":count}
    return render(request, "base/home.html", context)


def room(request, id):
    room = Room.objects.get(pk=id)
    return render(request, "base/room.html", context={"room": room})


def update_room(request, id):
    room = Room.objects.get(id=id)
    if request.method == "GET":
        form = RoomForm(instance=room)
        context = {"form": form}
        return render(request, "base/room_form.html", context=context)
    else:
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect("home")


def creat_room(request):
    if request.method == "GET":
        form = RoomForm()
        context = {"form": form}
        return render(request, "base/room_form.html", context=context)
    else:
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("home")


def delete_room(request, id):
    room = Room.objects.get(id=id)
    if request.method == "GET":
        context = {"obj": room}
        return render(request, "base/delete.html", context=context)
    else:
        room.delete()
        return redirect("home")
