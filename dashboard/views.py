from django.shortcuts import render, redirect
from .forms import *
from . models import Notes
from django.contrib import messages
from django.views import generic
import requests
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.decorators import login_required
from . forms import *
# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f"Notes Added from {request.user.username} Successfully")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)


@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes


# -------- Homework Section ------------#
@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finish = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished

            )
            homework.save()
            messages.success(request, f'Homework Added From {request.user.username}!!')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks': homework,
        'homework_dones': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)


@login_required
def update_homework(request, pk=None):
    homework = Homework.object.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished == True
    homework.save()
    return redirect('homework')


# views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Homework  # Assuming Homework is your model

def update_homework(request, pk=None):
    # Corrected this line to use 'objects' instead of 'object'
    homework = get_object_or_404(Homework, id=pk)
    
    if homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
    
    homework.save()
    return redirect('homework')  # Redirect to the homework page after updating


@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todo.save()
            messages.success(request, f"Todo Added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'form': form,
        'todos': todo,
        'todo_done': todo_done,
    }
    return render(request, 'dashboard/todo.html', context)

@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRatting'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }

        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username}!!")
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request,"dashboard/register.html", context)
@login_required
def profile(request):
    homework = Homework.objects.filter(is_finished=False, user=request.user)
    todo = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homework': homework,
        'todo': todo,
        'homework_done': homework_done,
        'todos_done': todos_done,
    }
    return render(request, 'dashboard/profile.html', context)


from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Redirect to homepage after login
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'dashboard/login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('login')  # Redirect to the login page or any other page you prefer

