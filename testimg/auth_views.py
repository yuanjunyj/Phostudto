from django.contrib import auth
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os

def login(request):
    if auth.get_user(request).username != '':
        return redirect('profile')
    return render(request, 'login.html')

def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return redirect('login')
    auth.login(request, user)
    user.current_visiting_path = ''
    user.save()
    return redirect('profile')

def signup(request):
    return render(request, 'signup.html')

def signup_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = User.objects.create_user(username=username, password=password)
        path = os.path.abspath(os.curdir).replace('\\', '/') + '/media/photos/' + str(user.id) + '/' + user.current_visiting_path
        os.mkdir(path)
        messages.info(request, 'Account registered successfully')  
        return redirect('login')
    except:
        messages.info(request, 'Username has already been picked')
        return redirect('signup')

@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout successfully') 
    return redirect('login')
