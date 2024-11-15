from django.shortcuts import render, redirect
from django.contrib.auth import logout
from sqlalchemy.orm import Session
from models_sqlalchemy import models, database
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from sqlalchemy.exc import SQLAlchemyError

# Dependency to create a session with SQLAlchemy
db_session = database.SessionLocal

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Start a session with SQLAlchemy
        try:
            db = db_session()
            user_record = db.query(models.User).filter(models.User.username == username).first()
            
            if user_record and user_record.hashed_password == password:
                # Assuming password hashing is not yet implemented. 
                # You can replace this with a hashed comparison logic.
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('landing_page')  # Redirecting to landing page instead of home page
                else:
                    error_message = 'Invalid username or password. Please try again.'
                    return render(request, 'auth_app/login.html', {'error_message': error_message})
            else:
                error_message = 'Invalid username or password. Please try again.'
                return render(request, 'auth_app/login.html', {'error_message': error_message})

        except SQLAlchemyError as e:
            # Handle any errors from SQLAlchemy
            error_message = f"Database error: {str(e)}"
            return render(request, 'auth_app/login.html', {'error_message': error_message})
        finally:
            db.close()  # Ensure that the session is closed

    return render(request, 'auth_app/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Home View
# @login_required
def home_view(request):
    return render(request, 'auth_app/home.html')

# Register View
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('landing_page')  # Redirecting to landing page instead of home page
    else:
        form = UserRegistrationForm()
    return render(request, 'auth_app/register.html', {'form': form})

# Landing Page View
@login_required
def landing_view(request):
    return render(request, 'auth_app/landing.html')
