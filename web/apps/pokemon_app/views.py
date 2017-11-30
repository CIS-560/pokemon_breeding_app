from django.shortcuts import render
from .models import Pokemon
from .models import Moves


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

