from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from .models import *
from github import Github
import git, os, subprocess

# Create your views here.
def home(request):
    return render(request, 'home.html')

# change to be just users listings
def user_profile(request):
	return render(request, 'user_profile.html', {'listings': Listing.objects.filter(user__id=request.user.id, open=True), 'favorites': Favorite.objects.filter(user__id=request.user.id)})

def detail(request, corgi_id):
    return render(request, 'browse.html', {'corgis': [Corgi.objects.get(id=corgi_id)]})

def browse_corgis(request):
    favorites = [fav.corgi.id for fav in Favorite.objects.filter(user=request.user)] if request.user.is_authenticated else []
    return render(request, 'browse.html', {
        'corgis': Corgi.objects.all(),
        'user': request.user,
        'favorites': favorites
    })

def buy_corgi(request):
    return render(request, 'buy.html', {'listings': Listing.objects.filter(open=True)})

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

def favorite_corgi(request):
    if request.method == 'POST':
        corgi = Corgi.objects.get(id=request.POST.get('corgi'))
        fav = Favorite.objects.filter(user=request.user, corgi=corgi)
        if not fav:
            Favorite.objects.create(user=request.user, corgi=corgi)
        else:
            fav[0].delete()
    return redirect('browse_corgis')

def close(request):
    if request.method == "POST":
        params = request.POST
        id = params['corgi_id']
        corgi = Listing.objects.get(corgi__id=id)
        corgi.open = False
        corgi.save()
    return redirect('user_profile')

def all_filter(request):
	if request.method == 'POST':
		params = request.POST
		gender = params['filter-gender']
		coloring = params['filter-coloring']
		state = params['filter-state']
		relation = params['filter-age']
		age = params['filter-year']

		where_flag = False;

		query = "select * from corgi_store_corgi"
		if(gender != "Any gender"):
			query+= " where gender ='"
			query+= gender
			query+="'"
			where_flag=True

		if(coloring != "Any coloring"):
			if(where_flag):
				query+=" and "
			else:
				query+=" where "
				where_flag=True
			query+="coloring='"
			query+=coloring
			query+="'"

		if(state != "Any state"):
			if(where_flag):
				query+=" and "
			else:
				query+=" where "
				where_flag = True
			query+="state='"
			query+=state
			query+="'"

		if(relation == "Greater than"):
			if(where_flag):
				query+=" and "
			else:
				query+=" where "
				where_flag = True
			query+="age_years >='"

		elif(relation == "Less than"):
			if(where_flag):
				query+=" and "
			else:
				query+=" where "
				where_flag = True
			query+="age_years <'"

		else:
			if(where_flag):
				query+=" and "
			else:
				query+=" where "
				where_flag = True
			query+="age_years ='"

		query+=age
		query+="'"

		return render(request, 'browse.html', {'corgis': Corgi.objects.raw(query)})

def buy_filter(request):
	if request.method == 'POST':
		params = request.POST
		gender = params['filter-gender']
		coloring = params['filter-coloring']
		state = params['filter-state']
		relation = params['filter-age']
		age = params['filter-year']
		lowPrice = params['filter-low-price']
		highPrice = params['filter-high-price']

		query = "select * from (corgi_store_listing join corgi_store_corgi on corgi_store_listing.corgi_id=corgi_store_corgi.id) where open=1"
		if(gender != "Any gender"):
			query+= " and gender ='"
			query+= gender
			query+="'"
			where_flag=True

		if(coloring != "Any coloring"):
			query+=" and coloring='"
			query+=coloring
			query+="'"

		if(state != "Any state"):
			query+=" and state='"
			query+=state
			query+="'"

		if(relation == "Greater than"):
			query+=" and age_years >='"

		elif(relation == "Less than"):
			query+=" and age_years <'"

		else:
			query+=" and age_years ='"

		query+=age
		query+="'"

		query+=" and price >= '"
		query+= lowPrice
		query+="' and price <='"
		query+= highPrice
		query+= "'"

		return render(request, 'buy.html', {'listings': Listing.objects.raw(query)})

def webhook(request):
    repo = git.Repo("/root/CSC346Project2")
    ref = request.POST['ref']
    if ref == "refs/heads/{}".format(repo.active_branch.name):
        repo.git.pull()
    return HttpResponse("Success")
