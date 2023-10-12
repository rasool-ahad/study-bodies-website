from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm
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
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "user does not exist")

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username or password is wrong")
            return render(request, "base/login_form.html")

def registerPage(request):
    form = MyUserCreationForm()
    context = {"form": form}
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
       
        return render(request, "base/registration_form.html", context)
    else :
        form = MyUserCreationForm(request.POST)
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
    activities = Message.objects.filter(Q(room__topic__name__icontains=search))[0:5]
    topic = Topic.objects.all()[0:5]
    count = rooms.count()
    context = {"rooms": rooms, "topics": topic, "count": count,"activities":activities}
    return render(request, "base/home.html", context)
def userProfile(request,id):
        user = User.objects.get(id=id)
        rooms = user.room_set.all()
        activities = user.message_set.all()
        topic = Topic.objects.all()
        context = {"rooms": rooms, "topics": topic,"activities":activities, 'user':user}
        return render(request, "base/user-profile.html", context)

def room(request, id):
    room = Room.objects.get(pk=id)
    comments = room.message_set.all()
    participents = room.participant.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participant.add(request.user)
        return redirect("room",id=room.id)
    context={"room": room, "comments": comments, "participents": participents}
    return render(request, "base/room.html", context )


@login_required(login_url="/login")
def update_room(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse("your not allowed here")
    if request.method == "GET":
        form = RoomForm(instance=room)
        topic = Topic.objects.all()
        context = {"form": form, "topics": topic , "room":room}
        return render(request, "base/room_form.html", context=context)
    else:
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")


        return redirect("home")


@login_required(login_url="/login")
def creat_room(request):
    if request.method == "GET":
        form = RoomForm()
        topic = Topic.objects.all()
        context = {"form": form, "topics": topic}
        return render(request, "base/room_form.html", context=context)
    else:
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get("name"),
            description = request.POST.get("description"),
        )
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

def delete_message(request,id):
    message = Message.objects.get(pk=id)
    if request.user != message.user:
        return HttpResponse("your not allowed here") 
    
    if request.method == "GET":
        context = {"obj": message}
        return render(request, "base/delete.html", context=context)
    else:
        message.delete()
        return redirect("home")

@login_required(login_url="login")
def updateUser(request):
    user = request.user
    if request.method == 'GET':
        form = UserForm(instance = user)
        context = {'form':form}
        return render(request, "base/update-user.html", context)
    else :
        form = UserForm(request.POST,request.FILES, instance= user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", id = request.user.id)

def topicsPage(request):
     search = request.GET.get("q", "") 
     topics = Topic.objects.filter(name__icontains=search)
     context = {'topics': topics}
     return render(request, "base/topics.html", context )

def activityPage(request):
    activities = Message.objects.all()
    context ={"activities":activities}
    return render(request, "base/activity.html", context)