from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import FoodListing, User, FoodClaim, Review
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.utils import timezone
import re
from django.db.models import Q
from .forms import DonorForm


def index(request):
    return render(request, 'index.html')

@login_required
def donor_dashboard(request):
    if not request.user.is_donor:
        messages.error(request, 'Access denied. Donor account required.')
        return redirect('web:index')
    
    # Get donor's food listings
    listings = FoodListing.objects.filter(donor=request.user).order_by('-created_at')
    
    context = {
        'listings': listings,
        'total_listings': listings.count(),
        'active_listings': listings.filter(is_available=True).count(),
    }
    return render(request, 'donor_dashboard.html', context)

@login_required
def collector_dashboard(request):
    if not request.user.is_collector:
        messages.error(request, 'Access denied. Collector account required.')
        return redirect('web:index')
    
    # Get available food listings
    listings = FoodListing.objects.filter(is_available=True).order_by('-created_at')
    
    # Get filter parameters
    food_type = request.GET.get('food_type')
    search = request.GET.get('search')
    
    if food_type:
        listings = listings.filter(food_type=food_type)
    if search:
        listings = listings.filter(
            Q(food_name__icontains=search) |
            Q(location__icontains=search)
        )
    
    context = {
        'listings': listings,
        'food_types': FoodListing.FOOD_TYPE_CHOICES,
    }
    return render(request, 'collector_dashboard.html', context)

def food_listings(request):
    listings = FoodListing.objects.filter(is_available=True).order_by('-created_at')
    
    # Get filter parameters
    food_type = request.GET.get('food_type')
    search = request.GET.get('search')
    
    if food_type:
        listings = listings.filter(food_type=food_type)
    if search:
        listings = listings.filter(
            Q(food_name__icontains=search) |
            Q(location__icontains=search)
        )
    
    context = {
        'listings': listings,
        'food_types': FoodListing.FOOD_TYPE_CHOICES,
    }
    return render(request, 'food_listings.html', context)

@login_required
def claim_food(request, listing_id):
    if not request.user.is_collector:
        messages.error(request, 'Only collectors can claim food.')
        return redirect('web:collector_dashboard')
        
    listing = FoodListing.objects.get(id=listing_id, is_available=True)
    if request.method == 'POST':
        listing.is_available = False
        listing.save()
        messages.success(request, 'Food claimed successfully!')
        return redirect('web:collector_dashboard')
    return render(request, 'claim_food.html', {'listing': listing})

@login_required
def my_listings(request):
    if request.user.is_donor:
        listings = FoodListing.objects.filter(donor=request.user)
    else:
        listings = FoodListing.objects.filter(is_available=True)
    
    return render(request, 'my_listings.html', {'listings': listings})

@login_required
def add_listing(request):
    if not request.user.is_donor:
        messages.error(request, 'Only donors can add food listings.')
        return redirect('web:index')
        
    if request.method == 'POST':
        # Get location data
        address = request.POST.get('address')
        city = request.POST.get('city')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Get food details
        food_type = request.POST.get('food_type')
        food_name = request.POST.get('food_name')
        quantity = request.POST.get('quantity')
        quality = request.POST.get('quality')
        
        if not all([address, city, food_type, food_name, quantity, quality]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('web:add_listing')
            
        try:
            # Create location string from address and city
            location = f"{address}, {city}"
            
            # Convert coordinates to Decimal if they exist
            lat = float(latitude) if latitude else None
            lng = float(longitude) if longitude else None
            
            listing = FoodListing.objects.create(
                donor=request.user,
                location=location,
                food_type=food_type,
                food_name=food_name,
                quantity=quantity,
                quality=quality,
                latitude=lat,
                longitude=lng
            )
            messages.success(request, 'Food listing added successfully!')
            return redirect('web:donor_dashboard')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('web:add_listing')
            
    return render(request, 'add_listing.html', {
        'food_types': FoodListing.FOOD_TYPE_CHOICES
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('web:index')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not email or not password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('web:login')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes
            messages.success(request, f'Welcome back, {user.name}!')
            return redirect('web:index')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('web:index')  # Redirect to index page for unregistered users
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        terms = request.POST.get('terms')

        print(f"Registration attempt - Name: {name}, Email: {email}, Phone: {phone}, User Type: {user_type}")

        # Validation
        if not all([name, email, phone, password, confirm_password, user_type, terms]):
            print("Missing required fields")
            messages.error(request, 'Please fill in all fields.')
            return redirect('web:register')

        if password != confirm_password:
            print("Passwords do not match")
            messages.error(request, 'Passwords do not match.')
            return redirect('web:register')

        if len(password) < 8:
            print("Password too short")
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('web:register')

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print("Invalid email format")
            messages.error(request, 'Please enter a valid email address.')
            return redirect('web:register')

        if not re.match(r'^\+?1?\d{9,15}$', phone):
            print("Invalid phone format")
            messages.error(request, 'Please enter a valid phone number.')
            return redirect('web:register')

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                name=name,
                phone=phone,
                user_type=user_type
            )
            print(f"User created successfully: {user.email}")
            login(request, user)
            messages.success(request, f'Welcome to EcoByte, {name}!')
            return redirect('web:index')
        except IntegrityError:
            print("Email already exists")
            messages.error(request, 'An account with this email already exists.')
            return redirect('web:register')
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            messages.error(request, 'An error occurred. Please try again.')
            return redirect('web:register')
    return render(request, 'register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('web:index')

@login_required
def delete_listing(request, listing_id):
    listing = FoodListing.objects.get(id=listing_id, donor=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('web:donor_dashboard')
    return render(request, 'delete_listing.html', {'listing': listing})

@login_required
def donor_form(request):
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.donor = request.user
            
            # Handle location data
            food_item.address = request.POST.get('address')
            food_item.city = request.POST.get('city')
            food_item.latitude = request.POST.get('latitude')
            food_item.longitude = request.POST.get('longitude')
            
            food_item.save()
            messages.success(request, 'Food item added successfully!')
            return redirect('web:donor_dashboard')
    else:
        form = DonorForm()
    return render(request, 'donor_form.html', {'form': form})