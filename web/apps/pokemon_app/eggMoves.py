from django.shortcuts import render 
from .models import Moves

def egg_moves(request):
    # filter egg moves that correspond to the chosen pokemon order by name
    egg_moves = Moves.objects.filter().order_by() 
    return #list of egg moves
