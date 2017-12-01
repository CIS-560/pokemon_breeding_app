from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Pokemon
from .models import Moves #, HistoryTrios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from .resources import TypeResource
from django.shortcuts import redirect 
from tablib import Dataset

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

        imported_data = dataset.csv.load(new_types.read())
        result = type_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            type_resource.import_data(dataset.csv, dry_run=False)  # Actually import now
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

