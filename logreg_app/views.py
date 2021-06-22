from django.shortcuts import render, redirect, HttpResponse
from time import localtime, strftime
import random
from .models import UserManager, User
from django.contrib import messages
import bcrypt

# ============ login/register page ========

def root(request):

    return render(request,'log.html')

# ============ redirect new user ==============

def register(request):

    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['firstname'],
            last_name = request.POST['lastname'],
            email = request.POST['email'],
            password = hashed,
        )

        request.session['userid'] = new_user.id

        return redirect('/success')

# ========= redirect existing user ==========

def login(request):

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    else:
        user = User.objects.filter(email = request.POST['log_email'])
        request.session['userid'] = user[0].id

    return redirect('/success')

# ============ logout =================

def logout(request):
    request.session.clear()
    return redirect('/')

# ============ landing page =================

def success(request):
    if "userid" not in request.session:
        
        messages.error(request, "Please log in before continuing!")
        
        return redirect('/')

    context = {
    "logged_in" :User.objects.get(id=request.session['userid'])
    }

    return render(request,'success.html',context)