from django.contrib import admin
from .models import Pokemon
from .models import Type
from .models import EggGroup 
from .models import Moves
from .models import Gender
from .models import LevelUpMove #, HistoryTrios
from import_export.admin import ImportExportModelAdmin
from .resources import PokemonResource, TypeResource, EggGroupResource, LevelUpMoveResource, MovesResource #, HistoryTriosResource

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Type)
admin.site.register(EggGroup)
admin.site.register(Gender)
admin.site.register(LevelUpMove)
admin.site.register(Moves)
# admin.site.register(HistoryTrios)

# @admin.register(Pokemon)
# @admin.register(EggGroup)
# @admin.register(LevelUpMove)
# @admin.register(HistoryTrios)
# @admin.register(Moves)
# class Pokemon(ImportExportModelAdmin):
#     import_id_fields = ('number')
# class Type(ImportExportModelAdmin):
#     model = Type
#     exclude = ('id', )
#     import_id_fields = ('type_num', )
#     skip_unchanged = True
#     fields = ['type_num', 'name']
# class EggGroup(ImportExportModelAdmin):
#     pass
# class LevelUpMove(ImportExportModelAdmin):
#     pass
# class HistoryTrios(ImportExportModelAdmin):
#     pass
# class Moves(ImportExportModelAdmin):
#     pass
