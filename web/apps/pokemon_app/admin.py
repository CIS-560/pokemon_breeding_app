from django.contrib import admin

from .models import Pokemon
from .models import Type
from .models import EggGroup 
from .models import Moves
from .models import Gender
from .models import LevelUpMove
# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Type)
admin.site.register(EggGroup)
admin.site.register(Gender)
admin.site.register(LevelUpMove)
admin.site.register(Moves)

