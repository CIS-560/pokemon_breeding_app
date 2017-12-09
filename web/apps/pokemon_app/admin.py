from django.contrib import admin
from .models import Pokemon
from .models import Type
from .models import EggGroup 
from .models import Moves
from .models import LevelUpMove , HistoryTrios, PokemonType

def type_names(self):
    return ', '.join([a.name for a in self.type.all()])
type_names.short_description = "Type Names"
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('name', type_names,)

# Register your models here.
admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(Type)
admin.site.register(EggGroup)
admin.site.register(LevelUpMove)
admin.site.register(Moves)
admin.site.register(PokemonType)
admin.site.register(HistoryTrios)

