from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Pokemon
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Moves, HistoryTrios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import redirect 

# Create your views here.
def app_entry(request):
    pokemons = Pokemon.objects.all()
    #moves = Moves.objects.all()
    return render(request, '../templates/homepage.html', {'pokemons': pokemons})
@csrf_exempt
def egg_moves(request):
    pokemon = request.POST['pokemon']
    
    egg_moves = Pokemon.objects.get(name=pokemon).egg_moves.all()
    egg_moves_list = []
    for i in egg_moves:
        print(i.name)
        egg_moves_list.append(i.name)
    if request.method == 'POST':
        return JsonResponse({'egg_moves': egg_moves_list}) 
        # return the egg moves that correspond to the chosen pokemon

def results(request):
    #male pokemon: male pokemon & ditto 
    #female pokemon: female pokemon or ungendered (if breeding with a ditto)
    female_pokemons = Pokemon.objects.filter(genders=2)
    male_pokemons = Pokemon.objects.filter(genders=1)
    pokemons = zip(female_pokemons, male_pokemons)
    return render(request, '../templates/results.html', {'pokemons':pokemons})

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

def favorites(request):
    history_trios = HistoryTrios.objects.all()
    #moves = Moves.objects.all()
    return render(request, '../templates/favorites.html', {'history_trios': history_trios})

