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
    return render(request, 'browse.html', {'title': 'Browse Corgis', 'corgis': Corgi.objects.all()})

def buy_corgi(request):
    return render(request, 'browse.html', {'title': 'Buy a Corgi', 'corgis': Corgi.objects.all()})

def list_corgi(request):
    return render(request, 'list_corgi.html')

def add_corgi(request):
    print("POST =", request.POST)
    user = get_object_or_404(User, pk=1)
    # user = request.user
    params = request.POST
    price = params['price'] if 'price' in params else None
    corgi = Corgi.objects.create(
        name=params['name'],
        age_years=params['years'],
        age_months=params['months'],
        gender=params['gender'],
        coloring=params['coloring'],
        city=params['city'],
        state=params['state'],
        owner=user,
        description=params['description']
    )
    return HttpResponse("Successfully added Corgi\n{}\n".format(corgi))
    # curl --data "name=spooky&age=3&gender=M&coloring=sable&location=tucson&description=cool&price=69000" http://127.0.0.1:8000/create_corgi/
    
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
