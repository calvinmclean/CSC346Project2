from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import *

# Create your views here.
def home(request):
    return render(request, 'home.html')

def detail(request, corgi_id):
    return render(request, 'browse.html', {'corgis': [Corgi.objects.get(id=corgi_id)]})

def browse_corgis(request):
    return render(request, 'browse.html', {'corgis': Corgi.objects.all()})

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
    return render(request, 'list_corgi.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.username = username
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
