from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Pokemon
from .models import Moves
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import redirect 

# Create your views here.
def app_entry(request):
    pokemons = Pokemon.objects.all()
    #moves = Moves.objects.all()
    return render(request, '../templates/homepage.html', {'pokemons': pokemons})

def results(request):
    #male pokemon: male pokemon & ditto 
    #female pokemon: female pokemon or ungendered (if breeding with a ditto)
    female_pokemons = Pokemon.objects.filter(genders=2)
    male_pokemons = Pokemon.objects.filter(genders=1)
    return render(request, '../templates/results.html', {'male_pokemon':male_pokemons, 'female_pokemon': female_pokemons})

def login(request):
    if request.POST:
        if 'login' in request.POST:
            return HttpResponseRedirect('/youloggedin/')
        else:
            return HttpResponseRedirect('/youregistered')
    else:
        return render(request, '../templates/login.html')
      
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, '../templates/register.html', {'form': form})

