from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from .forms import NoteForm
import sqlite3
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def login_user(request):

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login failed')
    
    #Helper variable to detect if we want the login or the register form
    context = {
        'page': 'login',
    }
    return render(request, 'base/login_register.html', context)

def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Registration failed, try again')

    return render(request, 'base/login_register.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

def home(request):
    form = NoteForm()
    #dummynotes to render in case user is not logged in
    dummy_notes = [
        {
            'title': 'Welcome to Awesome Notes!',
            'text': 'On this app, you will be able to create your own notes and read the notes of others.',
        },
        {
            'title': 'Trouble in Paradise?',
            'text': 'Be aware though, there is rumours going around that this app is terribly insecure...',
        },
        {
            'title': 'Did I say that outloud?',
            'text': 'Anyways, happy surfing, be sure to share all your sensitive data with us, we promise to keep it safe!',
        },
    ]

    context = {'form': form}
    
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
        context['notes'] = notes
    else:
        context['notes'] = dummy_notes

    return render(request, 'base/home.html', context)

@csrf_exempt
def create_note(request):
    
    # if request.method == 'POST':
    #     form = NoteForm(request.POST)
    #     if form.is_valid():
            
    #         form.save()
    #     else:
    #         messages.error(request, "Form data was not valid.")

    data = request.POST
    print(f"data is {data}")
    

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    print("CONNECTION ESTABLISHED")


    try:
        if data["private"] == "on":
            private = 1
    except:
        private = 0


    cursor.execute("INSERT INTO base_note (user_id, title, text, private, date_created) VALUES ('{}','{}','{}','{}', '{}');".format(data["user"], data["title"], data["text"], private, datetime.now()))
    connection.commit()
    connection.close()


    return redirect('home')

def delete_note(request, note_id):
    if request.user.is_authenticated:
        note = Note.objects.get(id=note_id)

        print(f"request.user.id is {request.user.id}, note.user_id is {note.user_id}")
        
        #if request.user.id == note.user_id:
        note.delete()
        return redirect('home')




def public(request):
    public_notes = Note.objects.filter(private=False)
    print(f"public notes is {public_notes}")
    context = {
        'notes': public_notes,
    }
    
    return render(request, 'base/public.html', context)
