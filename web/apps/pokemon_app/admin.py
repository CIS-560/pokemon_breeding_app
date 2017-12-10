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

class MovesAdmin(admin.ModelAdmin):
    list_display = ('move_num', 'name',)

class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_num', 'name',)
    
class EggGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'can_breed')

class LevelUpMoveAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'move', 'level')


# Register your models here.
admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(EggGroup, EggGroupAdmin)
admin.site.register(LevelUpMove, LevelUpMoveAdmin)
admin.site.register(Moves, MovesAdmin)
admin.site.register(HistoryTrios)

