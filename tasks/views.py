from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .form import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
  return render(request, 'home/home.html')

def signup(request):
  if request.method == 'GET':
    context = {'form':UserCreationForm}
    return render(request, 'signup/signup.html', context)
  else:
    if request.POST['password1'] == request.POST['password2']:
      # register user
      try:
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('tasks')
      except IntegrityError:
        context = {
          'form':UserCreationForm,
          'messageinfo':messages.info(request, 'El usuario ya existe')
          }
        return render(request, 'signup/signup.html', context)
    return render(request, 'signup/signup.html', {
          'form':UserCreationForm,
          'messagewarning': messages.warning(request, 'Las contraseñas no coinciden')
          })

@login_required
def tasks(request):
  tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
  return render(request, 'tasks/tasks.html', {'tasks':tasks})

@login_required
def tasks_completed(request):
  tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
  return render(request, 'tasks/tasks.html', {'tasks':tasks})

@login_required
def task_create(request):
  if request.method == 'GET':
    context = {'form':TaskForm}
    return render(request, 'tasks/task_create.html', context)
  else:
    try:
      form = TaskForm(request.POST)
      new_task = form.save(commit=False)
      new_task.user = request.user
      new_task.save()
      return redirect('tasks')
    except ValueError:
      context = {
        'form':TaskForm,
        'messageerror':messages.warning(request, 'Ingrese datos válidos')
        }
      return render(request, 'tasks/task_create.html', context)

@login_required
def task_detail(request, task_id):
  if request.method == 'GET':
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    form = TaskForm(instance=task)
    return render(request, 'tasks/task_detail.html', {'task':task, 'form':form})
  else:
    try:
      task = get_object_or_404(Task, pk=task_id, user=request.user)
      form = TaskForm(request.POST, instance=task)
      form.save()
      return redirect('tasks')
    except ValueError:
      return render(request, 'tasks/task_detail.html', {'task':task, 'form':form, 'error':'Error updating task'})

@login_required
def complete_task(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def delete_task(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.delete()
    return redirect('tasks')

@login_required
def cerrarSesion(request):
  logout(request)
  return redirect('home')

def iniciarSesion(request):
  if request.method == 'GET':
    context = {
    'form':AuthenticationForm
    }
    return render(request, 'signin/signin.html', context)
  else:
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
      context = {
          'form':AuthenticationForm,
          'messageinfo':messages.warning(request, 'El usuario o contraseña no existen')
          }
      return render(request, 'signin/signin.html', context)
    else:
      login(request, user)
      return redirect('tasks')