from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def loginPage(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(request, "base/login_form.html")

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username or password is wrong")
            return render(request, "base/login_form.html")

def registerPage(request):
    form = UserCreationForm()
    context = {"form": form}
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
       
        return render(request, "base/registration_form.html", context)
    else :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else : 
            messages.error(request, "some error happend during registration")
            return render(request, "base/registration_form.html", context)

            

def logoutPage(request):
    logout(request)
    return redirect("home")



def home(request):
    search = request.GET.get("q", "")
    rooms = Room.objects.filter(Q(topic__name__icontains=search) |
                                Q(host__username__icontains=search) |
                                Q(description__icontains=search))
    topic = Topic.objects.all()
    count = rooms.count()

    context = {"rooms": rooms, "topics": topic, "count": count}
    return render(request, "base/home.html", context)


def room(request, id):
    room = Room.objects.get(pk=id)
    return render(request, "base/room.html", context={"room": room})


@login_required(login_url="/login")
def update_room(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse("your not allowed here")
    if request.method == "GET":
        form = RoomForm(instance=room)
        context = {"form": form}
        return render(request, "base/room_form.html", context=context)
    else:
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect("home")


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def delete_room(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse("your not allowed here")
    if request.method == "GET":
        context = {"obj": room}
        return render(request, "base/delete.html", context=context)
    else:
        room.delete()
        return redirect("home")
