from import_export import resources
from .models import Type, Moves, EggGroup, Pokemon, LevelUpMove #, HistoryTrios 

class TypeResource(resources.ModelResource):
    class Meta:
        model = Type
        exclude = ('id', )
        import_id_fields = ('type_num', )
        skip_unchanged = True
        fields = ['type_num', 'name']

class MovesResource(resources.ModelResource):
    class Meta:
        model = Moves

class EggGroupResource(resources.ModelResource):
    class Meta:
        model = EggGroup

class PokemonResource(resources.ModelResource):
    class Meta:
        model = Pokemon

class EggGroupResource(resources.ModelResource):
    class Meta:
        model = EggGroup

class LevelUpMoveResource(resources.ModelResource):
    class Meta:
        model = LevelUpMove

# class HistoryTriosResource(resources.ModelResource):
#     class Meta:
#         model = HistoryTrios


