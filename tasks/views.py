from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages

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
        context = {
          'form':UserCreationForm,
          'messagesuccess':messages.success(request, 'Usuario creado correctamente')
          }
        return render(request, 'signup/signup.html', context)
      except:

        context = {
          'form':UserCreationForm,
          'messageinfo':messages.info(request, 'El usuario ya existe')
          }
        return render(request, 'signup/signup.html', context)
    return render(request, 'signup/signup.html', {
          'form':UserCreationForm,
          'messagewarning': messages.warning(request, 'Las contraseñas no coinciden')
          })
