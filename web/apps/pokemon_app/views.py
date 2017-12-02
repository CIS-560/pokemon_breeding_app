from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Pokemon, Type, LevelUpMove
from .models import Moves #, HistoryTrios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from .resources import TypeResource
from django.shortcuts import redirect 
from tablib import Dataset
import pandas as pd 

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

def simple_upload(request):
    if request.method == 'POST':
        type_resource = TypeResource()
        dataset = Dataset()
        new_types = request.FILES['myfile']

        #imported_data = dataset.csv.load(new_types.read())
        result = type_resource.import_data(dataset, dry_run=True)  # Test the data import

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
                print('added ' + str(col1_val) + ' ' + str(col2_val)) 
        elif check_names == ('poke_num', 'level_up_move_num'):
            column_3_dataframe = csv[['level']]
            for value in range(csv.shape[0]):
                col1_val = int(column_1_dataframe.at[value,col_names[0]])
                col2_val = int(column_2_dataframe.at[value,col_names[1]])
                poke = Pokemon.objects.get(number= col1_val)
                move = Moves.objects.get(move_num= col2_val)
                the_level = int(column_3_dataframe.at[value, 'level'])
                LevelUpMove.objects.create(poke_number= poke, move_num=move, level=the_level)
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
    return render(request, '../templates/import.html')

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
