from django.apps import AppConfig
import pandas as pd
from apps.pokemon_app.models import Pokemon

class PokemonAppConfig(AppConfig):
    name = 'pokemon_app'
    
