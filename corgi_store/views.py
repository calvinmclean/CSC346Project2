from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from .models import *

# Create your views here.
def home(request):
    return render(request, 'home.html')

# change to be just users listings 
def user_profile(request):
	return render(request, 'user_profile.html', {'listings': Listing.objects.filter(user__id=request.user.id, open=True )})
	
def detail(request, corgi_id):
    return render(request, 'browse.html', {'corgis': [Corgi.objects.get(id=corgi_id)]})

def browse_corgis(request):
    return render(request, 'browse.html', {'corgis': Corgi.objects.all(), 'user': request.user})

def buy_corgi(request):
    return render(request, 'buy.html', {'listings': Listing.objects.all()})

def list_corgi(request):
    if request.method == "POST":
        user = request.user
        params = request.POST
        corgi = Corgi.objects.create(
            name=params['name'],
            age_years=params['age_years'],
            age_months=params['age_months'],
            gender=params['gender'],
            coloring=params['coloring'],
            city=params['city'],
            state=params['state'],
            description=params['description']
        )
        # TODO: I can do this once 'listradio' is fixed
        # corgi = Corgi.objects.create(**params, owner=user)
        if int(params['price']):
            listing = Listing.objects.create(
                user=user,
                corgi=corgi,
                price=params['price'],
                contact=params['contact']
            )
        return redirect('browse_corgis')
        
    if request.user.is_authenticated:
    	return render(request, 'list_corgi.html')
    else:
    	form = AuthenticationForm()
    	return render(request, 'registration/login.html', {'modal_message': 'Please login to list a corgi','form':form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            try:
                form.save()
            except IntegrityError:
                return render(request, 'sign_up.html', {'form': form, 'integrity_error': 'Email {} already in use.'.format(username)})
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.username = username
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
    
def close(request):
	    if request.method == "POST":
	        params = request.POST
	        id = params['corgi_id']
	        corgi = Listing.objects.get(corgi__id=id)
	        corgi.open = False
	        corgi.save()
	        return render(request, 'user_profile.html', {'listings': Listing.objects.filter(user__id=request.user.id, open=True )})

