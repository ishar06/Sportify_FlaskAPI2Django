from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, AddressForm
from .models import Address
import requests

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Get username from email
        try:
            user = User.objects.get(email=email)
            username = user.username
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Get the next parameter or default to index
                next_url = request.POST.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist')
    
    # If GET request or authentication failed, redirect to home
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validate passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('index')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('index')
        
        username = email
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.first_name = name
        user.save()
        Address.objects.create(user=user, house_street="", pincode="", state="")

        messages.success(request, 'Registration successful! Please log in.')

    return redirect('index')

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


@login_required
def profile(request):
    if request.method == 'POST':
        if 'update_user' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Your personal information has been updated!')
                return redirect('profile')
            else:
                for field, errors in u_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        u_form = UserUpdateForm(instance=request.user)
    
    addresses = Address.objects.filter(user=request.user)
    context = {
        'u_form': u_form,
        'addresses': addresses,
    }
    return render(request, 'user_app/profile.html', context)

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', 'id')
    return render(request, 'user_app/address_list.html', {'addresses': addresses})

@login_required
def address_create(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'user_app/address_form.html', {'form': form, 'title': 'Add New Address'})

@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'user_app/address_form.html', {'form': form, 'title': 'Edit Address'})

@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if address.is_default:
        messages.error(request, "Cannot delete default address!")
        return redirect('address_list')
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('address_list')

@login_required
def set_default_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    Address.objects.filter(user=request.user).update(is_default=False)
    address.is_default = True
    address.save()
    messages.success(request, 'Default address updated successfully!')
    return redirect('address_list')


def index(request):
    # Your existing index view code
    # ...
    
    # Add user profile data if user is authenticated
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = {
                'username': request.user.username,
                'name': request.user.first_name or request.user.username,
                'email': request.user.email,
                'date_joined': request.user.date_joined,
                'address': request.user.address if hasattr(request.user, 'address') else None
            }
        except:
            pass
    
    context = {
        # Your existing context
        # ...
        'user_profile': user_profile,
    }
    
    return render(request, 'index.html', context)


def about(request):
    try:
        # Fetch content from Flask API
        response = requests.get('http://127.0.0.1:5000/api/about')
        response.raise_for_status()
        flask_content = response.json()['content']
        return render(request, 'user_app/about.html', {'flask_content': flask_content})
    except Exception as e:
        return render(request, 'user_app/about.html', {'error': str(e)})


def blogs(request):
    try:
        # Add timeout to prevent hanging
        response = requests.get('http://127.0.0.1:5000/api/blogs', timeout=5)
        
        # Check if the response was successful
        if response.status_code != 200:
            error_message = f'Error fetching content: HTTP {response.status_code}'
            if response.status_code == 500:
                error_message = 'Internal Server Error: Please make sure the Flask server is running correctly'
            return render(request, 'user_app/blogs.html', {'error': error_message})
            
        flask_content = response.json()['content']
        return render(request, 'user_app/blogs.html', {'flask_content': flask_content})
    except requests.Timeout:
        return render(request, 'user_app/blogs.html', {
            'error': 'Request timed out. Please check if the Flask server is running.'
        })
    except requests.ConnectionError:
        return render(request, 'user_app/blogs.html', {
            'error': 'Could not connect to Flask server. Please make sure it is running.'
        })
    except Exception as e:
        return render(request, 'user_app/blogs.html', {'error': str(e)})

