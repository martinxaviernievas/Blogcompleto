from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone

def home(request):
    return render(request, 'home.html',)

def signup(request):
    
    if request.method == 'GET':
       return render(request, 'signup.html', {
        'form': UserCreationForm()  
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user =  User.objects.create_user(username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm(),
                    "error": 'User alredy exists'
                })

        return render(request, 'signup.html', {
                'form': UserCreationForm(),
                "error": 'Password do not match'  
    })



def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks':tasks})
    
    

def create_task(request):

    if request.method == 'GET':
         return render(request,'create_task.html',{
            'form': TaskForm
        })

    else:
        try:
            form =  TaskForm(request.POST)
            new_task= form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_task.html',{
            'form': TaskForm,
            'error':'Please provide valid date'
        })

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form })
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        else:
            return render(request, 'task_detail.html', {'task': task, 'form': form})

def complete_task(request, task_id):
  task = get_object_or_404(Task,pk=task_id,user=request.user)
  if request.method == 'POST':
        task.datecompleted= timezone.now()
        task.save()
        return redirect('tasks')
  
def delete_task(request, task_id):
  task = get_object_or_404(Task,pk=task_id,user=request.user)
  if request.method == 'POST':
        task.delete()      
        return redirect('tasks')  

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method =='GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
         })
    else:
         user = authenticate(
             request, username=request.POST['username'], password=request.POST
             ['password'])
         if user is None:
             return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or passwoed is incorrect'
            })
         else:
             login(request, user)
             return redirect('tasks')
    