from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Message, Room, Game
from .forms import RoomForm
from django.contrib.auth.models import User


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User name or password does not exist')

    context = {'page': page}
    return render(request, 'core/login_register.html', context)


def registerPage(request):
    form = UserCreationForm
    context = {'form': form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'core/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    rooms_count = rooms.count()
    games = Game.objects.all()
    context = {
        'rooms': rooms,
        'games': games,
        'q': q,
        'rooms_count': rooms_count

    }
    return render(request, 'core/home.html', context)


def room(request, pk):

    try:
        room = Room.objects.get(id=pk)
        room_messages = room.message_set.all().order_by('-created')
        participants = room.participants.all()
        if request.method == 'POST':
            messages = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body'))
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
        context = {
            'rooms': room,
            'room_messages': room_messages,
            'participants': participants
        }
    except:
        context = {
            'rooms': False
        }
    

    return render(request, 'core/room.html', context)


# ---------------------------CRUD Room--------------------------------------

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'core/room_form.html', context)


@login_required(login_url='login')
def updaeRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'core/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': room})

# ---------------------------Search Component in Navnar--------------------------------------


def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Room.objects.filter(
        Q(topic__name__icontains=query_original) |
        Q(name__icontains=query_original)
    )
    print(queryset)
    mylist = []
    mylist += [i.name for i in queryset]

    print(mylist)
    return JsonResponse(mylist, safe=False)

# ---------------------------Message managment--------------------------------------
    
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': message})