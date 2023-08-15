from django.shortcuts import render,redirect,reverse, get_object_or_404
from django.http import HttpResponse
from .models import Room, Topic,Message,User
from .form import RoomForm,UserForm,NewUserCreationForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def userLogin(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get('password')
        
        user = authenticate(request, username= username, password=password)
        if user is not None:
            login(request, user)
            direct = request.GET.get("next") if request.GET.get("next") != None else "home"
            return redirect(direct)
        else:
            messages.error(request,"invalid details")
    context = {"page":page}
    return render(request, "base/login_reg.html",context)

def userLogout(request):
    logout(request)
    direct = request.GET.get("next") if request.GET.get("next") != None else "home"
    return redirect(direct)

def registerPage(request):
    form = NewUserCreationForm()
    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.username = user.username.lower()
            user.save()     
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Account creation failed")
    context = {"form":form}
    return render(request, "base/login_reg.html", context)

# @login_required(login_url="login")
def home(request):
    search = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=search) |
        Q(name__icontains=search) |
        Q(description__icontains=search)
        )
    total_room = Room.objects.all()
    topic = Topic.objects.annotate(room_count=Count('room')).order_by('-room_count')
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains = search)
        )
    context = {
        "rooms":rooms,
        "topics":topic,
        "room_count":room_count,
        "room_messages":room_messages,
        "total_room":total_room
    }
    return render(request, "base/home.html",context)

# @login_required(login_url="login")
def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all().order_by("-id")
    room.participants.add(room.host)
    
    if request.method == "POST" and request.user.is_authenticated:
        body= request.POST.get("body")
        room.participants.add(request.user)
        if body:
            message = Message.objects.create(user= request.user, room= room , body=body)
            message.save()
            return redirect('room',pk = room.id)
    context = {"room": room, "room_messages":room_messages,"participants":participants}
    return render(request, "base/room.html",context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    is_follower = user.followers.filter(id=request.user.id).exists()
    room_messages = user.message_set.all()
    rooms = user.participants.all()
    topics = Topic.objects.all()
    total_room = Room.objects.all()
    context = {
        "room_messages":room_messages,
        "topics":topics,
        "rooms":rooms,
        "total_room":total_room,
        "user":user,
        'is_follower': is_follower
    }
    return render(request, "base/profile.html",context)

@login_required(login_url="login") 
def userUpdate(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect("user",user.id)
    context = {
        "form":form
    }
    return render(request, "base/user_update.html",context)

@login_required(login_url="login")    
def createRoom(request):
    page = "create"
    room = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic = request.POST.get("topic")
        name = request.POST.get("name")
        description = request.POST.get("description")
        
        topic,create = Topic.objects.get_or_create(name=topic)
        new_room  = Room.objects.create(
            host = request.user,
            name=name,
            topic=topic,
        )
        new_room.participants.add(request.user)
        new_room.save()
        return redirect("home")
    context = {
        "form":room,
        "topics":topics,
        "page":page
               }
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    current_topic = room.topic
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return redirect("home")
    
    if request.method == 'POST':
        topic = request.POST.get("topic")
        name = request.POST.get("name")
        description = request.POST.get("description")
        
        topic,create = Topic.objects.get_or_create(name=topic)
        
        room.topic = topic
        room.name = name
        room.description = description
        room.save()
        topic_count = current_topic.room_set.all().count()
        if topic_count == 0:
            current_topic.delete()
        return redirect("home")
    context = {
        "form":form,
        "room":room,
        "topics":topics
        }
    
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")   
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    topic = room.topic
    if request.user != room.host:
        return redirect("home")
    
    if request.method=='POST':
        #delete the post from database using object's delete method
        room.delete()
        topic_count = topic.room_set.all().count()
        if topic_count == 0:
            topic.delete()
        return redirect("home")
    
    return render(request, "base/delete_room.html",{"room":room})


@login_required(login_url="login")   
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    room = (message.room)
    if request.user != message.user:
        return redirect("home")
    
    if request.method=='POST':
        #delete the post from database using object's delete method
        message.delete()
        url = reverse("room", args=[room])
        return redirect(url)
    
    return render(request, "base/delete_room.html",{"room":room})

def topicPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains = q).annotate(room_count = Count("room")).order_by("-room_count")
    rooms = Room.objects.all()
    context = {
        "topics":topics,
        "rooms":rooms
    }
    return render(request, "base/topics.html",context)

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html",{"room_messages":room_messages})

@login_required(login_url="login")
def follow(request,pk):
        current_user = request.user
        user = get_object_or_404(User,id = pk)
        if user is not None:
            if request.user == user:
                return redirect("user",pk=pk)
            
            user.followers.add(current_user)
            current_user.following.add(user)
            current_user.save()
            user.save()
        return redirect("user",pk=pk)
    

@login_required(login_url="login")
def unfollow(request, pk):
    user = get_object_or_404(User, id=pk)
    current_user = request.user

    if request.user in user.followers.all():
        user.followers.remove(current_user)
        current_user.following.remove(user)

    return redirect("user", pk=pk)
    
        
    