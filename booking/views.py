from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Booking
from .forms import BookingForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('booking:index')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = UserCreationForm()
    return render(request, 'booking/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('booking:index')
            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid login details.')
    return render(request, 'booking/login.html')

@login_required
def index(request):
    bookings = Booking.objects.filter(customer__user=request.user)
    return render(request, 'booking/index.html', {'bookings': bookings})

@login_required
def book(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user.customer
            booking.save()
            messages.success(request, 'Booking successful.')
            return redirect('booking:index')
    else:
        form = BookingForm()
    return render(request, 'booking/book.html', {'form': form})