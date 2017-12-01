from django.shortcuts import render
from .models import Pokemon
from .models import Moves
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def app_entry(request):
    pokemons = Pokemon.objects.all()
    #moves = Moves.objects.all()
    return render(request, '../templates/homepage.html', {'pokemons': pokemons})
@csrf_exempt
def egg_moves(request):
    pokemon = request.POST['pokemon']
    
    print("\n\n\n")

    egg_moves = Pokemon.objects.get(name=pokemon).egg_moves.all()
    egg_moves_list = []
    for i in egg_moves:
        print(i.name)
        egg_moves_list.append(i.name)
    if request.method == 'POST':
        return JsonResponse({'egg_moves': egg_moves_list}) 
        # return the egg moves that correspond to the chosen pokemon

        

