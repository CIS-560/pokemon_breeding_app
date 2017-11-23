from django.db import models

class Type(models.Model):
    type_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)


class Moves(models.Model):
    move_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

class Gender(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Genderless'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

class EggGroup(models.Model):
    name = models.CharField(max_length=15, primary_key=True)
    can_breed = models.BooleanField(default=False)



class Pokemon(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=1000)
    is_evolved = models.BooleanField(default=False)
    type = models.ManyToManyField(Type)
    level_up_moves = models.ManyToManyField(Moves, through='LevelUpMove')
    egg_moves = models.ManyToManyField(Moves, related_name='%(class)s_egg_move')
    genders = models.ManyToManyField(Gender)
    egg_groups = models.ManyToManyField(EggGroup)


#this is an example of an intermediate table in django, 
#it refers to the instace of specifc pokemon, levelup_move
#and it provides additional information about Level_move
class LevelUpMove(models.Model):
    poke_number = models.ForeignKey(Pokemon)
    move_num = models.ForeignKey(Moves)
    level = models.IntegerField()  # this doesn't need to be unique




class User(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=15)

class HistoryTrios(models.Model):
    # id field is automatically generated by django :)

    # users can make many HistoryTrios
    # but a historyTrio can only be associated with one user
    username = models.ForeignKey(User)

    # should these pokemon be many-to-many or many-to-one
    parent1 = models.ForeignKey(Pokemon, related_name='%(class)s_parent_1')
    parent2 = models.ForeignKey(Pokemon, related_name='%(class)s_parent_2')
    child = models.ForeignKey(Pokemon, related_name='%(class)s_child')

    # relation on these?
    parent_level_up_move = models.ForeignKey(Moves, related_name='%(class)s_parent_level_up_move')
    child_egg_move = models.ForeignKey(Moves, related_name='%(class)s_child_egg_move')
