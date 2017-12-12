from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Pokemon, Type, LevelUpMove
from .models import Moves, HistoryTrios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import redirect 
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from tablib import Dataset
from django import forms
import pandas as pd 
import ast
import json

# Create your views here.
@csrf_exempt
def app_entry(request):
    if request.method == 'POST':
        # pokemon = request.GET.get('pokemon')
        # pokemon_obj_name = Pokemon.objects.get(name = pokemon)
        # print(pokemon_obj_name)
        #moves = Moves.objects.all()
        selecter_poke = request.POST.get('pokemon_select')
        selected_move = request.POST.get('egg_move_select');
        selected_name = Moves.objects.get(name= selected_move)
#        print('pokemon', selecter_poke, 'move', selected_move)
        # selected = Pokemon.objects.get(name = selected_pokemon)
        return redirect(request, 'results')
    pokemons = Pokemon.objects.all()
    return render(request, '../templates/homepage.html', {'pokemons': pokemons})

@csrf_exempt
def egg_moves(request):
    pokemon = request.POST['pokemon']
    egg_moves = Pokemon.objects.get(name=pokemon).egg_moves.all()
    egg_moves_list = []
    for i in egg_moves:
#        print(i.name)
        egg_moves_list.append(i.name)
    if request.method == 'POST':
        return JsonResponse({'egg_moves': egg_moves_list}) 
        # return the egg moves that correspond to the chosen pokemon

@csrf_exempt
def add_to_favorites(request):
    if request.user.is_authenticated():
        username = request.user.username    
        user = User.objects.get(username=username)

    male = request.POST.get('male_pokemon')
    female = request.POST.get('female_pokemon')
    child = request.POST.get('child')
    move = request.POST.get('egg_move')
    level = int(request.POST.get('level'))
    pokemon = request.POST.get('pokemon')

    # select query for all necessary pokemon goes here 
    male_pokemon = Pokemon.objects.get(name=male)
    female_pokemon = Pokemon.objects.get(name=female)
    child_pokemon = Pokemon.objects.get(name=child)
    move_pokemon = Moves.objects.get(name=move)
    level_up = LevelUpMove.objects.get(level=level, 
                                       pokemon=male_pokemon, 
                                       move=move_pokemon) 
    egg_move = Moves.objects.get(name=move)  
 
    if request.method == 'POST':
        #insert query for history trios goes here
        HistoryTrios.objects.create(username=user,
                                    parent1=male_pokemon,
                                    parent2=female_pokemon,
                                    child=child_pokemon,
                                    parent_level_up_move=move_pokemon,
                                    child_egg_move=egg_move)
    return JsonResponse({'child': child, 'move':move}) 
        # return the egg moves that correspond to the chosen pokemon
        
@csrf_exempt
def get_values(request):
    selected_move = request.POST.get('egg_move_select')
    selected_poke = request.POST.get('pokemon-select')
    print('we have',selected_poke,'with',selected_move)
    return redirect('results' )

#male pokemon: male pokemon & ditto 
#female pokemon: female pokemon or ungendered (if breeding with a ditto)
def results(request):
    for key, value in request.POST.items():
        print(key, value)
    selected_move = request.POST.get('egg_move_select')
    selected_poke = request.POST.get('pokemon')
    temp = selected_poke[4::].split(".",1)[0]
#    print('we have',temp,'with',selected_move)
    poke = Pokemon.objects.get(name=temp) 

    #get egg move in question
    move = Moves.objects.get(name= selected_move)
    female_pokemons = [poke]

    # male_pokemons= Pokemon.objects.filter(level_up_moves=move).exclude(male_ratio=0)
    male_pokemons = LevelUpMove.objects.filter(move=move).exclude(pokemon__male_ratio=0)
    return render(request, '../templates/results.html', {'male_pokemon':male_pokemons, 'female_pokemon': female_pokemons})

def simple_upload(request):
    if request.method == 'POST':
        new_types = request.FILES['myfile']

        #django.setup()
        csv = pd.read_csv(request.FILES['myfile'])
        col_names = list(csv.columns.values)
        #the first column name will be for pokemon
        pokemon_model_att = ''
        model_att = ''
        #get the model variables based off of column names
        check_names = (col_names[0], col_names[1])

        column_1_name = col_names[0] 
        column_2_name = col_names[1] 
        
        column_1_dataframe = csv[[col_names[0]]]
        print(column_1_dataframe)
        column_2_dataframe = csv[[col_names[1]]]
        #print(poke_num)
        #print(type_num)
        already_checked = [] 

        if check_names == ('poke_num', 'type_num'):
            for value in range(csv.shape[0]):
                col1_val = int(column_1_dataframe.at[value,col_names[0]])
                col2_val = int(column_2_dataframe.at[value,col_names[1]])
                Pokemon.objects.get(number= col1_val).type.add(col2_val)
                print('poke_typ added ' + str(col1_val) + ' ' + str(col2_val)) 
        elif check_names == ('poke_num', 'level_up_move_num'):
            column_3_dataframe = csv[['level']]
            for value in range(csv.shape[0]):
                col1_val = int(column_1_dataframe.at[value,col_names[0]])
                col2_val = int(column_2_dataframe.at[value,col_names[1]])
                poke = Pokemon.objects.get(number= col1_val)
                move = Moves.objects.get(move_num= col2_val)
                the_level = int(column_3_dataframe.at[value, 'level'])
                LevelUpMove.objects.create(pokemon = poke, move=move, level=the_level)
                print('poke_level_up_move added ' + str(col1_val) + ' ' + str(col2_val)) 
        elif check_names == ('poke_num', 'egg_move_num'):
            for value in range(csv.shape[0]):
                col1_val = int(column_1_dataframe.at[value,col_names[0]])
                col2_val = str(column_2_dataframe.at[value,col_names[1]])
                Pokemon.objects.get(number= col1_val).egg_moves.add(col2_val)
                print('poke_egg_move added ' + str(col1_val) + ' ' + str(col2_val)) 
        elif check_names == ('number', 'name'):
            column_3_dataframe = csv[['description']]
            column_4_dataframe = csv[['is_evolved']]
            column_5_dataframe = csv[['male_ratio']]
            column_6_dataframe = csv[['female_ratio']]
            column_7_dataframe = csv[['picture']]
            for value in range(csv.shape[0]):
                col1_val = int(column_1_dataframe.at[value,col_names[0]])
                col2_val = str(column_2_dataframe.at[value,col_names[1]])
                col3_val = str(column_3_dataframe.at[value,'description'])
                
                val = str(column_4_dataframe.at[value,'is_evolved'])
                col4_val = str_to_bool(val)
                col5_val = str(column_5_dataframe.at[value,'male_ratio'])
                col6_val = str(column_6_dataframe.at[value,'female_ratio'])
                col7_val = str(column_7_dataframe.at[value,'picture'])
                Pokemon.objects.create(number= col1_val, name=col2_val, description=col3_val, is_evolved=col4_val, male_ratio= col5_val, female_ratio=col6_val, picture=col7_val)
                print('pokemon added ' + str(col1_val) + ' ' + str(col2_val)) 
        else:
            for value in range(csv.shape[0]):
                col1_val = int(column_1_dataframe.at[value,col_names[0]])
                col2_val = str(column_2_dataframe.at[value,col_names[1]])
                Pokemon.objects.get(number= col1_val).egg_groups.add(col2_val)
                print('poke_egg_group_added ' + str(col1_val) + ' ' + str(col2_val)) 
    return render(request, '../templates/import.html')

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False

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

def parse(request):
    #django.setup()
    csv = pd.read_csv('poke_type_cleaned.csv')
    col_names = list(csv.columns.values)
    #the first column name will be for pokemon
    pokemon_model_att = ''
    model_att = ''
    #get the model variables based off of column names
    check_names = (col_names[0], col_names[1])

    column_1_name = col_names[0] 
    column_2_name = col_names[1] 
    
    column_1_dataframe = csv[[col_names[0]]]
    print(column_1_dataframe)
    column_2_dataframe = csv[[col_names[1]]]
    #print(poke_num)
    #print(type_num)
    already_checked = [] 

    if check_names == ('poke_num', 'type_num'):
        for value in range(csv.shape[0]):
            col1_val = int(column_1_dataframe.at[value,col_names[0]])
            col2_val = int(column_2_dataframe.at[value,col_names[1]])
            Pokemon.objects.get(number= col1_val).type.add(col2_val)
            print('added ' + str(col1_val) + ' ' + str(col2_val)) 
    elif check_names == ('poke_num', 'level_up_move_num'):
        for value in range(csv.shape[0]):
            col1_val = int(column_1_dataframe.at[value,col_names[0]])
            col2_val = int(column_2_dataframe.at[value,col_names[1]])
            poke = Pokemon.objects.get(number = col1_val)
            move = Moves.objects.get(move_num = col2_val ) 
             
            Pokemon.objects.get(number= col1_val).level_up_moves.add(col2_val)
            print('added ' + str(col1_val) + ' ' + str(col2_val)) 
    elif check_names == ('poke_num', 'egg_move_num'):
        for value in range(csv.shape[0]):
            col1_val = int(column_1_dataframe.at[value,col_names[0]])
            col2_val = int(column_2_dataframe.at[value,col_names[1]])
            Pokemon.objects.get(number= col1_val).egg_moves.add(col2_val)
            print('added ' + str(col1_val) + ' ' + str(col2_val)) 
    elif check_names == ('poke_num', 'genders'):
        for value in range(csv.shape[0]):
            col1_val = int(column_1_dataframe.at[value,col_names[0]])
            col2_val = int(column_2_dataframe.at[value,col_names[1]])
            Pokemon.objects.get(number= col1_val).genders.add(col2_val)
            print('added ' + str(col1_val) + ' ' + str(col2_val)) 
    else:
        for value in range(csv.shape[0]):
            col1_val = int(column_1_dataframe.at[value,col_names[0]])
            col2_val = int(column_2_dataframe.at[value,col_names[1]])
            Pokemon.objects.get(number= col1_val).egg_groups.add(col2_val)
            print('added ' + str(col1_val) + ' ' + str(col2_val)) 
    return render(request, '../templates/login.html')
