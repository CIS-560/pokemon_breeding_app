from django.shortcuts import render
from .models import Pokemon
from .models import Moves


# Create your views here.
def app_entry(request):
    pokemons = Pokemon.objects.all()
    #moves = Moves.objects.all()
    return render(request, '../templates/homepage.html', {'pokemons': pokemons})

