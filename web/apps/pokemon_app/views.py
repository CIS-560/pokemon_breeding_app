from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Pokemon, Type, LevelUpMove
from .models import Moves #, HistoryTrios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import redirect 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from tablib import Dataset
import pandas as pd 
import ast
import json

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
