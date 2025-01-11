from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from My_project import settings
from django.core.mail import send_mail



def home(request):
    return render(request,"home.html")

def user_login(request): 
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
             messages.error(request, "Username already exist! Please try another username!")
             return redirect('signup')
        
        if User.objects.filter(email=email):
             messages.error(request, "Email alrady Registered")
             return redirect('signup')
        
        if len(username)>15:
             messages.error(request, "Username must be under 15 characters")
            
        if pass1 != pass2:
             messages.error(request, "Password didn't match")

        if not username.isalpha():
             messages.error(request, "Username must be Alpha-Numeric!")
             return redirect('signup')
    
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been created succesfully.")

        subject = "Welcome to Emusic Family"
        message = "Hello" + myuser.first_name + "!! /n" + "Welcome to Emusic Application!! /n Thank you for Registered"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        

        return redirect('login')

    return render(request,"signup.html")

def signout(request):
        logout(request)
        messages.success(request, "Logged out Successfully")
        return redirect('home')

def dashboard(request):
     return render(request,"dashboard.html")

def settings(request):
     return render(request,"settings.html")

def profile(request):
     return render(request,"profile.html")

def helpcenter(request):
     return render(request,"helpcenter.html")
