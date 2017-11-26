# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-22 22:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryTrios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_child', to='pokemon_app.Pokemon')),
                ('child_egg_move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_child_egg_move', to='pokemon_app.Moves')),
                ('parent1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_parent_1', to='pokemon_app.Pokemon')),
                ('parent2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_parent_2', to='pokemon_app.Pokemon')),
                ('parent_level_up_move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_parent_level_up_move', to='pokemon_app.Moves')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='pokeegggroup',
            name='child_egg_move',
        ),
        migrations.AddField(
            model_name='historytrios',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon_app.User'),
        ),
    ]
